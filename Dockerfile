FROM python:3.11-slim AS builder

WORKDIR /app
RUN pip install --no-cache-dir uv

# Copy only dependency files first for better cache usage
COPY pyproject.toml uv.lock* ./

RUN uv venv --clear
RUN uv pip install .

COPY main.py ./
COPY src ./src
COPY config ./config

FROM python:3.11-slim AS final

WORKDIR /app

COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH" 

CMD ["python", "-m", "main"]
