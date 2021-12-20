FROM python:alpine

COPY main.py luci.py requirements.txt /app/
WORKDIR /app

ENTRYPOINT ["/bin/python", "main.py"]