# Choose the base image
FROM python:3.8.10
# set the working directory
WORKDIR /app
# copy the requirements file to /app
COPY requirements.txt requirements.txt
# install the requirements
RUN pip install -r requirements.txt
# copy files
COPY . .
# expose a port
EXPOSE 8000
# start the app
CMD ["python3", "manage.py", "runserver"]
