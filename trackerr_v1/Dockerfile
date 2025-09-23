# Use the base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install dependencies for psycopg2 and others
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# copy requirements
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
# Copy the project files
COPY . /app/
#exposed port
EXPOSE 8000

# Start the app using Gunicorn
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

