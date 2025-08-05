# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file if you have one
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (if your app runs a web server, e.g., Flask on 5000)
EXPOSE 5000

# Set default command (replace app.py with your main script)
CMD ["python", "app.py"]