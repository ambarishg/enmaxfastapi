FROM python:3.8-slim-buster
COPY . /app
WORKDIR /app
RUN pip3 install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]