# pull official base image
FROM python:3.10.6-alpine

# Update pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# set work directory
WORKDIR /usr/src/qadam

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Create and activate a virtual environment
RUN python -m venv venv
ENV PATH="/usr/src/qadam/venv/bin:$PATH"

# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# Start your application here
