# AI Resume Analyzer

Backend-first FastAPI MVP for uploading resumes, extracting text, analyzing them with AWS Bedrock, validating structured JSON, and rendering server-side HTML reports.

## Stack

- Python 3.12+
- FastAPI
- Jinja2 templates
- Tailwind CSS via CDN
- SQLAlchemy 2.0
- Alembic
- SQLite by default, PostgreSQL-ready through `DATABASE_URL`
- AWS Bedrock for AI inference

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

## Configure AWS Bedrock

Enable access to your selected Bedrock model in the AWS console, then configure local AWS credentials. For development, the AWS CLI is the simplest option:

```bash
aws configure
```

Set an AWS region and a Bedrock model ID in `.env`:

```env
AWS_REGION=us-east-1
AI_MODEL=anthropic.claude-3-5-haiku-20241022-v1:0
```

The application uses the standard AWS credential provider chain: AWS CLI credentials, environment variables, or an IAM role in AWS. Never add access keys to `.env` or commit them. Change `AI_MODEL` to any model enabled for your account and region that supports the Bedrock Converse API.

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

For AWS App Runner deployment:

You have two options:

1. Source code deploy using `apprunner.yaml`.
2. Container deploy using the included `Dockerfile`.

For the source code path, App Runner can build directly from the repo with the included `apprunner.yaml`.

Set these runtime environment variables:

```env
AWS_REGION=ap-southeast-1
AI_MODEL=apac.amazon.nova-lite-v1:0
APP_ENV=production
APP_DEBUG=false
LOG_LEVEL=INFO
```

Notes:

- Use environment variables for all configuration.
- Store secrets in App Runner secrets or AWS Secrets Manager.
- Use S3 instead of local `uploads` for durable file storage.
- Use PostgreSQL through RDS or Aurora if you want persistence.
- Grant the App Runner instance role permission to invoke the configured Bedrock model.
- If you only want a demo host right now, local SQLite and local uploads are enough for a first deployment.
- App Runner passes `PORT` automatically, so the app must listen on `0.0.0.0:8080`, which is what the config file uses.
