# Usage: docker build -t not-enough-musk-spambot .
#        docker run not-enough-musk-spambot
#        docker run -it not-enough-musk-spambot /bin/bash

# Importing python image
FROM python:3.12-slim-bookworm

# Setting working directory
WORKDIR /app

# Copying all files from current directory
COPY ../../sql /app/sql
COPY ../../src /app/src
COPY ../../requirements.txt /app/requirements.txt
COPY ../../phrases.py /app/phrases.py
COPY ../../read_comments.py /app/read_comments.py

# Installing required packages
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Running python code
ENTRYPOINT ["python", "read_comments.py"]