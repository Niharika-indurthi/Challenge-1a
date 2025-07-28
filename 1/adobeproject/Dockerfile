FROM python:3.9-slim
RUN apt-get update && apt-get install -y tesseract-ocr libpoppler-dev poppler-utils
RUN pip install --no-cache-dir pdf2image pytesseract beautifulsoup4
WORKDIR /app
COPY main.py /app/
CMD ["python", "main.py"]