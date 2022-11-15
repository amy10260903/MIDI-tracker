FROM python:3.8.13-slim-buster

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/list*

WORKDIR /app
COPY deploy ./
RUN pip3 install -r requirements.txt && \
    chown -R 1001:0 /app && \
    chmod -R g=u /app

RUN ["chmod", "+x", "docker-entrypoint.sh"]
ENTRYPOINT ["sh", "./deploy/docker-entrypoint.sh"]
CMD ["python", "./midi_tracker/manage.py", "runserver", "0.0.0.0:8000"]