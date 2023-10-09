FROM python:3.9-buster
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    curl \
    openjdk-11-jdk \
    ruby-full

RUN mkdir -p /app

COPY src/main /app/src/main
COPY *.sh /app/
COPY *.py /app/
COPY ci/version /app/ci/version
COPY scripts /app/scripts
COPY requirements.txt /app/requirements.txt
# COPY fluent.conf /fluentd/etc/fluent.conf

WORKDIR /app

# RUN chmod +x scripts/fluent.sh
RUN chmod +x bootstrap.sh
RUN chmod +x start.sh
# RUN scripts/fluent.sh
RUN ./bootstrap.sh

# CMD ["./start.sh"]
CMD ["ls -la"]

EXPOSE 80
