FROM python:3.12-alpine

RUN apk update && apk add --no-cache \
    shadow \
    bash \
    && rm -rf /var/cache/apk/*

RUN useradd -ms /bin/bash appuser

WORKDIR /app

RUN chown -R appuser:appuser /app
RUN mkdir -p /var/logs && chown -R appuser:appuser /var/logs

USER appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
