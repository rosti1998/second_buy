# Use the official Python image as base
FROM python:3.9-slim


# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory


# Copy requirements file
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project


# Expose port for the Django development server
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
