FROM python:3.12-slim

WORKDIR /app/OpenManus

RUN apt-get update && apt-get install -y --no-install-recommends git curl \
    && rm -rf /var/lib/apt/lists/* \
    && (command -v uv >/dev/null 2>&1 || pip install --no-cache-dir uv)

COPY . .

RUN uv pip install --system -r requirements.txt

ENTRYPOINT ["streamlit", "run", "/app/OpenManus/openmanus/app.py", "--server.address", "0.0.0.0", "--server.port", "8000"]
