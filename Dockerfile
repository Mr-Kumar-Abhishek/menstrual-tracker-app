FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive \
    POETRY_VIRTUALENVS_CREATE=false \
    KIVY_NO_ARGS=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libgl1 \
    libgles2 \
    libglib2.0-0 \
    libmtdev1 \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    xclip \
    xsel \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml ./
RUN poetry install --no-interaction --no-ansi

COPY . .

CMD ["xvfb-run", "-a", "pytest", "-v"]

