# Deployment Guide

This project is intended for local development and portfolio demonstration.

## Local API

```bash
pip install -r backend/requirements-dev.txt
uvicorn app.main:app --app-dir backend --reload
```

## Docker Compose

```bash
docker compose up --build
```

The API is available at `http://localhost:8000`.

## Runtime Data

- Synthetic source documents live in `sample-data/`.
- Local Chroma files are written under `backend/data/chroma/`.
- JSONL audit logs are written under `logs/`.

Do not mount production healthcare data, patient records, payer member files, or proprietary policy manuals into this project.
