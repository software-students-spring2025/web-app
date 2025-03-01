# Use Python 3.10 base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy dependencies first for better caching
COPY requirements.txt . 

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set Flask environment variables using .env
COPY .env . 

# Expose port 5000 for Flask
EXPOSE 5000

# Run the application with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
