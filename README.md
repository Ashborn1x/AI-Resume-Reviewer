# AI Resume Analyzer

Backend-first FastAPI MVP for uploading resumes, extracting text, analyzing them with a local Ollama LLM, validating structured JSON, and rendering server-side HTML reports.

## Stack

- Python 3.12+
- FastAPI
- Jinja2 templates
- Tailwind CSS via CDN
- SQLAlchemy 2.0
- Alembic
- SQLite by default, PostgreSQL-ready through `DATABASE_URL`
- Ollama for local development

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Create the database:

```bash
alembic upgrade head
```

Start the app:

```bash
uvicorn app.main:app --reload
```

Or, on Windows with the local virtual environment:

```powershell
.\scripts\start_dev_server.ps1
```

Open `http://127.0.0.1:8000`.

## Configure Ollama

Install and start Ollama, then pull any supported model:

```bash
ollama pull llama3.1
ollama serve
```

Set the model in `.env`:

```env
AI_PROVIDER=ollama
AI_MODEL=llama3.1
OLLAMA_BASE_URL=http://localhost:11434
```

Model names are never hardcoded in the application. Change `AI_MODEL` to use Llama, Qwen, Mistral, Gemma, or another local model available in Ollama.

## Changing AI Providers

AI access is isolated under `app/ai`. The application calls `AIService`, which delegates to a provider created by `create_ai_provider`.

To add Bedrock, OpenAI, or Anthropic later:

1. Implement `AIProvider` in `app/ai/providers/`.
2. Register the provider in `app/ai/provider_factory.py`.
3. Set `AI_PROVIDER` in `.env`.

No route, parser, prompt, or template code should need to change.

## Prompt Management

Prompts live in `app/prompts/*.md` and are loaded through `PromptManager`.

Current prompts:

- `resume_analysis.md`
- `ats_review.md`
- `recruiter_review.md`
- `rewrite_resume.md`
- `job_match.md`

## Upload Pipeline

```text
Upload -> Validate -> Save -> Extract Text -> Clean -> Normalize -> AI Analysis -> Validate JSON -> Render HTML
```

Supported formats:

- PDF
- DOCX
- TXT

Upload limits and allowed extensions are configured in `.env`.

## Migrations

Create a migration:

```bash
alembic revision --autogenerate -m "describe change"
```

Run migrations:

```bash
alembic upgrade head
```

Switching to PostgreSQL should only require installing the driver and changing `DATABASE_URL`, for example:

```env
DATABASE_URL=postgresql+psycopg://user:password@host:5432/resume_analyzer
```

## Tests

```bash
pytest
```

The app is structured for dependency injection so services, parsers, repositories, and AI providers can be tested independently.

## AWS App Runner Notes

For a later App Runner deployment:

- Use environment variables for all configuration.
- Store secrets in AWS Secrets Manager or App Runner secrets.
- Use S3 instead of local `uploads` for durable file storage.
- Use PostgreSQL through RDS or Aurora.
- Add a production AI provider such as Bedrock behind the existing provider interface.
