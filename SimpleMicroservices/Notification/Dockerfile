FROM python:3-slim
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY notificationServer.py ./
COPY .env ./
CMD [ "python", "./notificationServer.py" ]
