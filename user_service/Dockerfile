# Base Image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port (default Django port)
EXPOSE 8002

# Start the Django server
CMD ["python", "manage.py", "runserver", "127.0.0.1:8002"]
