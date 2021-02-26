FROM q267009886/fastapi-poetry:python3.7-alpine3.8

WORKDIR /app

# Copy using poetry.lock* in case it doesn't exist yet
COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root --no-dev

COPY . .
