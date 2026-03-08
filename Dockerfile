FROM python:3.11-slim

LABEL maintainer="iceccarelli"
LABEL description="Palletizer Full Stack — open-source palletising software"

WORKDIR /app

# Install dependencies
COPY pyproject.toml README.md ./
COPY palletizer_full/ palletizer_full/

RUN pip install --no-cache-dir -e .

# Default command runs the demo
CMD ["python", "-m", "palletizer_full.run"]
