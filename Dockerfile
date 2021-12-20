FROM ubuntu:20.04

COPY main.py luci.py requirements.txt /app/
WORKDIR /app


# Install python
RUN apt-get update && \
    apt-get install -y python pip && \
    pip install -y requirements.txt && \
    apt-get clean && \
    rm -rf \
      /tmp/* \
      /var/lib/apt/lists/* \
      /var/tmp/*

ENTRYPOINT ["/bin/python", "main.py"]