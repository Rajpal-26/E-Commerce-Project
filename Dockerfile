FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# expose the port the Flask app uses
EXPOSE 5000

CMD ["python", "run.py"]