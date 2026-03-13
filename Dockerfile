from python:3.12-slim

workdir /app

copy . . 

run pip install --no-cache-dir -r requirements.txt

expose 5000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]