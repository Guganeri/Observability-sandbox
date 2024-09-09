FROM python:3.9.19-bullseye
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["ddtrace-run", "python", "main.py"]