# GitHub Recruiter Tool

## A recruiter-facing tool that takes a GitHub username and returns AI-generated assessments of each public repository — complexity level, documentation quality, and an experience signal — to help hiring managers screen candidates without reading every README manually.

## Tech Stack

**Backend** (from `backend/requirements.txt`):

- Python / FastAPI (≥0.115)
- uvicorn (≥0.32)
- httpx (≥0.27) — async GitHub API client
- openai (≥1.55) — Structured Outputs via `chat.completions.parse`
- pydantic (≥2.10) — API schemas and LLM response schema
- python-dotenv (≥1.0)

**Frontend** (from `frontend/package.json`):

- React 19
- TypeScript ~6.0
- Vite 8
- axios 1.18

**AI configuration** (from `backend/config.py`):

- Model: `gpt-4o-mini`
- Temperature: `0.2`

---

## Architecture

```
User input (username or GitHub URL)
    │
    ▼
Username normalization (client + server)
    │
    ▼
GitHub API — verify user exists
    │
    ▼
GitHub API — fetch repos (per_page=100, sort=updated)
    │
    ▼
Filter forks → cap at 10 repos
    │
    ▼
GitHub API — fetch READMEs concurrently (asyncio.gather)
    │
    ▼
OpenAI — one Structured Outputs call per repo, concurrently
    │
    ▼
JSON response → React dashboard (3-column card grid)
```

**This is a structured single-call AI integration per repo, not an autonomous agent.** For each repository I send one system prompt, one user message (README + metadata), and receive one schema-validated JSON object. There is no tool-calling loop and no multi-step planning where the model decides what to do next. I chose this because the task is well-defined — assess one repo from known evidence — and a single call is the right level of complexity for an MVP screening tool. An agent-style design would add latency, cost, and unpredictability without improving the output for this use case.

---

## Key Design Decisions

### Fork filtering

I exclude forked repositories before applying the repo cap. A fork reflects someone else's project, not the candidate's original work, and including forks would dilute the hiring signal. The alternative — keeping forks but labeling them — adds noise to a recruiter-facing view without much benefit at this scale.

### Repo cap (10)

I set `MAX_REPOS_TO_ANALYZE = 10` in `config.py`. Each repo triggers a separate OpenAI call, so analyzing an unbounded list would be slow and expensive. Repos are already sorted by most-recently-updated from GitHub, so the cap keeps the most relevant recent work. The alternative — analyzing every public repo — would work for small portfolios but degrades for prolific GitHub users.

### README length handling

I set `MAX_README_CHARS = 15_000` in `config.py`. This is a **safety guardrail**, not routine trimming. The README is the primary evidence the model assesses, so I set the cap high enough that typical candidate READMEs pass through whole. My `truncate_readme()` function only cuts content when it exceeds that limit (e.g. pathological changelog dumps on forked repos) and appends a truncation notice. The alternative — a low cap like 2,000 characters — would routinely cut meaningful documentation and hurt assessment quality.

### Structured Outputs vs. free-text JSON

I use `client.chat.completions.parse()` with `response_format=RepoAssessmentLLM` so OpenAI enforces the schema at the API level. The response is guaranteed to match my Pydantic model — no regex parsing or JSON repair. I split `RepoAssessmentLLM` (fields the model infers) from `RepoAssessment` (full API row including `repo_name` and `has_readme` from GitHub). The alternative — asking the model to "return JSON" in plain text — is brittle when labels must be consistent for a hiring UI.

### Calibration in the system prompt

I wrote explicit calibration rules in `SYSTEM_PROMPT`: prefer the lower plausible label when evidence is ambiguous, require strong proof before "Advanced", treat README marketing language as non-evidence, and keep summaries factual. I did this because inflated AI assessments are harmful in hiring — a recruiter who trusts flattering over-ratings makes worse decisions than one who gets conservative ratings. Without explicit instructions, models tend toward generous labels.

I set temperature to 0.2 for the AI calls. Lower temperature reduces creative variation and keeps labels consistent across repos — the same project assessed twice should get the same complexity_level. High temperature makes sense for creative writing; it's wrong for an evaluation task where consistency is the goal.

### No-README handling

When a repo has no README (or empty content), I **skip the OpenAI call** and return null judgment fields with the summary `"No README available — assessment skipped."` I deliberately do not assign "Poor" or "Beginner" because that would imply I assessed something when I had no documentation. The alternative — calling the model on metadata alone — risks fabricated project narratives from repo name and star count alone.

### Per-repo failure isolation

I run AI assessments with `asyncio.gather(..., return_exceptions=True)`. If one repo hits an OpenAI timeout or rate limit, the rest still return. Failed repos get null judgment fields plus an `assessment_error` message on that card. I also run GitHub README fetches concurrently with `asyncio.gather` for the same latency reason.

### Badge colors

In `badgeTones.ts`, complexity uses gray / blue / green (Beginner / Intermediate / Advanced) and documentation uses rose / amber / green (Poor / Adequate / Excellent). Badges always show the text label, not color alone. Complexity uses a neutral tiered palette (gray/blue/green) because Beginner is descriptive, not a flaw — a well-scoped junior project should not show a red badge. Documentation quality uses a warning-style palette (rose/amber/green) because poor documentation is a genuine signal worth flagging visually. Both badges include a text label so the encoding works for colorblind users.

### Frontend state and HTTP

I used plain React `useState` — three UI states and one API response do not justify Redux or Zustand. I used axios for the single analyze endpoint because I prefer its error handling over manual `fetch` status checks. Styling is plain CSS per component (no Tailwind) to keep the UI easy to read in review.

### Input normalization (client + server)

Both the frontend and backend normalize usernames and profile URLs. The server is the source of truth; the client normalizes too because profile URLs cannot be sent literally in `/api/analyze/{username}` path segments.

### Output Format

I chose a card-based layout with separate badges for complexity_level and documentation_quality because these are independent signals — a Beginner project with excellent documentation is meaningfully different from a Beginner project with no README, but a single field can't express that. Color-coded badges let a recruiter extract both signals across ten cards in seconds without reading every word.

---

## Setup & Run Instructions

### Prerequisites

- Python 3.9+ (tested locally; no version pinned in repo)
- Node.js 18+ (required by Vite 8)
- A GitHub Personal Access Token
- An OpenAI API key

### Backend

```bash
cd backend

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

python3 -m pip install -r requirements.txt

cp .env.example .env
# Edit backend/.env — see table below

python3 -m uvicorn main:app --reload --port 8000
```

Backend runs at **http://localhost:8000**. Interactive API docs: **http://localhost:8000/docs**

**Required environment variables** (`backend/.env`):

| Variable         | Description                                                                                                                                                                                         |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GITHUB_TOKEN`   | GitHub Personal Access Token. No scopes needed for public read-only data; raises rate limit to ~5,000 requests/hour. If the their is not Access token, the system will work with the basic api call |
| `OPENAI_API_KEY` | OpenAI API key. **Required** for all AI assessments.                                                                                                                                                |

### Frontend

```bash
cd frontend

npm install
npm run dev
```

Frontend runs at **http://localhost:5173**.

**Start the backend first**, then the frontend. Vite proxies `/api` to `http://localhost:8000` (see `frontend/vite.config.ts`), so no extra CORS setup is needed in local development.

No frontend `.env` is required for local dev.

### End-to-end test

1. Open http://localhost:5173
2. Enter `torvalds` and click **Analyze** (or press Enter)
3. After several seconds you should see a results header and a grid of repo cards (up to 10 non-fork repos)
4. Each assessed card shows complexity and documentation badges, a summary, and an experience signal
5. Repos without a README show **"No README — assessment skipped"** instead of badges

---

## API Reference

| Method | Path                      | Description                                                |
| ------ | ------------------------- | ---------------------------------------------------------- |
| `GET`  | `/health`                 | Health check — returns `{"status": "ok"}`                  |
| `GET`  | `/api/repos/{username}`   | GitHub fetch only (no AI). Returns repos with README text. |
| `GET`  | `/api/analyze/{username}` | Full pipeline: GitHub fetch + AI assessment per repo.      |

The `username` path parameter accepts a bare username, `@username`, or a `https://github.com/username` URL. Normalization runs on the server (and on the client before building the request URL).

---

## Known Limitations

- **Single-page repo fetch** — `per_page=100` with no pagination. Candidates with more than 100 public repos may have older work omitted before filtering.
- **Fixed cap of 10 repos** — only the most recently updated non-fork repos are assessed.
- **No automated test suite** — `test_*.py` files in `backend/` are manual run scripts, not pytest/CI.
- **No API authentication** — anyone who can reach the backend can trigger GitHub and OpenAI usage. Not production-ready as-is.
- **Dev proxy only** — no backend CORS or production API URL configuration yet; the frontend expects `/api` on the same origin or a proxy.
- **README guardrail** — READMEs over 15,000 characters are truncated before sending to OpenAI.

---

## AI Tools Used in Building This

I used **Cursor** for implementation scaffolding and in-editor development, and **Claude** for architecture discussion, prompt design, and phase-by-phase explanations. I reviewed and typed the code myself to make sure I understood each layer — GitHub fetching, structured outputs, calibration rules, and the React dashboard — rather than shipping generated code I could not explain in an interview.

---

## Future Development Ideas

### Job-description-aware assessment

Right now every repo is assessed against general criteria. A natural extension — especially for a recruiting product — would let a recruiter paste a job description alongside the GitHub username. I would thread that description into the system and user prompts and add a `relevance_to_role` field to the structured output schema. That would shift the tool from "describe this candidate's projects" to "does this candidate fit **this opening**," which is closer to how recruiters actually work.

### Pagination for prolific users

The current single-page GitHub fetch can miss repos beyond the first 100. For active open-source contributors, adding pagination with a configurable upper bound would make the tool more reliable for the candidates where automated screening matters most.

### Side-by-side candidate comparison

When narrowing finalists, recruiters often compare two profiles directly. A view that accepts two usernames and renders assessments side-by-side would turn the tool from a per-candidate lookup into a ranking aid for later pipeline stages.

---

**Author:** Liran Hozias
