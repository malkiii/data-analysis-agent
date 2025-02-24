FROM python:3.10-slim

WORKDIR /usr/src/app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "app.py"]