# Use the base image
FROM python:3.8.10

# Set the working directory
WORKDIR /app
# copy requirements
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
# Copy the project files
COPY . /app/
#exposed port
EXPOSE 8000

# Start the app using Gunicorn
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

