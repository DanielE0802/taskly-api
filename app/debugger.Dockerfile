FROM python:3.12-slim-bookworm

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
EXPOSE 5678

ENV DEBUG=false

CMD ["/bin/sh", "-c", "\
  if [ \"$DEBUG\" = 'true' ]; then \
    python3 -m debugpy --listen 0.0.0.0:5678 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000; \
  else \
    uvicorn main:app --reload --host 0.0.0.0 --port 8000; \
  fi"]