# IMDB Sentiment Analysis

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135.1-green.svg)](https://fastapi.tiangolo.com/)
[![Gradio](https://img.shields.io/badge/Gradio-4.8.0-orange.svg)](https://gradio.app/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

IMDB movie review sentiment analysis using Logistic Regression. The model determines whether a review is positive or negative and shows prediction confidence.

## 🌐 Live demo (try it!)

- **Gradio interface**: [https://huggingface.co/spaces/dotwired/imdb-gradio](https://huggingface.co/spaces/dotwired/imdb-gradio)
- **API docs**: [https://dotwired-imdb-fastapi.hf.space/docs](https://dotwired-imdb-fastapi.hf.space/docs)
- **Health check**: [https://dotwired-imdb-fastapi.hf.space/health](https://dotwired-imdb-fastapi.hf.space/health)

## Demo

- **Gradio Interface**: http://localhost:7860
- **FastAPI Documentation**: http://localhost:8000/docs

## Features

- Model accuracy: **89.9%** on test set
- Fast predictions (<100ms)
- Rate limiting (100 requests per minute)
- Docker ready
- Interactive Gradio UI
- Automatic API documentation (Swagger)

## Tech Stack

- **ML**: scikit-learn (Logistic Regression)
- **Backend**: FastAPI
- **Frontend**: Gradio
- **Validation**: Pydantic
- **Containerization**: Docker
- **Security**: slowapi (rate limiting)

## Installation & Setup

### Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/uwaspwned/imdb-sentiment-analysis.git
cd imdb-sentiment-analysis/imdb-model-gui

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # for Linux/Mac

# or

.venv\Scripts\activate     # for Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train the model (or download pre-trained)
python model.py

# 5. Run FastAPI
uvicorn main:app --reload

# 6. In another terminal, run Gradio
python gradio_app.py
```

### Run with Docker (recommended)

```bash
# 1. Clone the repository
git clone https://github.com/uwaspwned/imdb-sentiment-fastapi.git
cd imdb-sentiment-analysis/imdb-model-gui

# 2. Start with one command
docker-compose up --build

# 3. Open in browser
# Gradio: http://localhost:7860
# FastAPI: http://localhost:8000/docs
```
