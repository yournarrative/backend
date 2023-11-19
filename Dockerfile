FROM python:3.11-slim

# UPDATE CONTAINER
RUN apt-get update
RUN apt-get install -y build-essential

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
#ENV STAGE=$STAGE

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

RUN poetry install

COPY . .

WORKDIR /app/service/src/interview_analyzer

CMD ["python", "./main.py"]
