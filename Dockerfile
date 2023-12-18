FROM python:3.9-slim

# UPDATE CONTAINER
RUN apt-get update
RUN apt-get install -y build-essential

ARG PORT=5001
ARG HOST="0.0.0.0"

ENV PORT=$PORT
ENV HOST=$HOST

EXPOSE $PORT

# STANDARD PYTHON SETUP
ENV PYTHONWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100
ENV POETRY_VERSION=1.4.0
ENV PYTHONPATH="/app/service/src/interview_analyzer:/app/service/src"

# INSTALL DEPENDENCIES
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

WORKDIR /app/service
COPY . .
RUN poetry install

# RUN APP
WORKDIR /app/service/
CMD ["gunicorn", "--config", "src/interview_analyzer/gunicorn.conf.py", "src.interview_analyzer.main:app"]
