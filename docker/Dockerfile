FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY exporter/ exporter/

EXPOSE 9100

ENTRYPOINT ["python", "-m", "exporter.server"]
CMD ["--port", "9100", "--interval", "5"]
