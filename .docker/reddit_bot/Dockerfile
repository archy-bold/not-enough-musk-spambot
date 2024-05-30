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
COPY ../../reddit_bot.py /app/reddit_bot.py

# Installing required packages
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Running python code
CMD ["python", "reddit_bot.py"]