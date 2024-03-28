
FROM python:3-slim
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY enrollment.py ./
COPY .env ./
CMD [ "python", "enrollment.py" ]
