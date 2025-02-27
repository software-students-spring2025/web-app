FROM python:3.13-slim

WORKDIR /app

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies using pipenv
RUN pipenv install --deploy --system

# Copy application code
COPY . .

# Expose port from env
EXPOSE 8000

# Use gunicorn for production or flask for development
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
