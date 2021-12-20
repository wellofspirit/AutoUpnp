FROM python:alpine

COPY main.py luci.py requirements.txt /app/
WORKDIR /app

# Install Dependencies
RUN pip install -y requirements.txt

ENTRYPOINT ["/bin/python", "main.py"]