FROM python:3.11-alpine

# Create a working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache postgresql-dev gcc musl-dev

# Copy your application code
COPY api.py .
COPY app.py .

# Install Python dependencies
RUN pip install psycopg2 fastapi uvicorn

# Run FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]


