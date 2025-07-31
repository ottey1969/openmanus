FROM python:3.12-slim

# Set WORKDIR directly to the directory containing app.py
WORKDIR /app/OpenManus/openmanus

RUN apt-get update && apt-get install -y --no-install-recommends git curl \
    && rm -rf /var/lib/apt/lists/* \
    && (command -v uv >/dev/null 2>&1 || pip install --no-cache-dir uv)

# Copy the contents of the \'openmanus\' directory into the WORKDIR
COPY openmanus .

RUN uv pip install --system -r requirements.txt

# Use CMD to run Streamlit, as WORKDIR is now correct
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8000"]
