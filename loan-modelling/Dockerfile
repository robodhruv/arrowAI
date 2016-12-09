FROM arrowai/graphlab:v5
ADD . /app
WORKDIR /app
CMD gunicorn app:app -t 4000

EXPOSE 8000

