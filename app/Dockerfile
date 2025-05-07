# Use Python 3.11 official image
FROM python:3.11

# Set working directory inside container
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy backend files explicitly
COPY main.py /app/
COPY database.py /app/
COPY models.py /app/
COPY schemas.py /app/
COPY routes/ /app/routes/
COPY __init__.py /app/

# Set PythonPath
ENV PYTHONPATH="/app"

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
