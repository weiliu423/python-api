# 1 
FROM python:3.10.6

# 2
RUN pip install Flask gunicorn flask_restful  google-cloud-storage firebase firebase_admin pandas

# 3
COPY src/ /app
WORKDIR /app

# 4
ENV PORT 5000

# 5
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app