FROM python:3.9-slim

WORKDIR /opt/api

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python", "api.py"]
