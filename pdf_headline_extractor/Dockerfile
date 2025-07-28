FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY extract_outline.py /app/

RUN pip install --no-cache-dir pdfminer.six langdetect

ENTRYPOINT ["python", "extract_outline.py"]
