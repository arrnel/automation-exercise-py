FROM python:3.13-slim

ENV TZ=Europe/Moscow \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    MPLBACKEND=Agg

WORKDIR /app

RUN mkdir /test_temp_files && \
    apt-get update && apt-get install -y \
    curl \
    build-essential \
    git \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libreadline-dev \
    xvfb && \
    rm -rf /var/lib/apt/lists/* && \
    curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-ansi --with dev

COPY . .

ENTRYPOINT ["sh", "-c"]
CMD ["pytest tests --alluredir=/allure-results -m \"$PYTEST_MARK_EXPR\" $PYTEST_ARGS"]
