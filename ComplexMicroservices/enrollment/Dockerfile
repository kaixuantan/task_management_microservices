
FROM python:3-slim
COPY requirements.txt ./

RUN python -m pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y wait-for-it

# Change the permissions of the wait-for-it.sh script
RUN chmod +x ./wait-for-it.sh

COPY enrollment.py ./
COPY .env ./

EXPOSE 5000

CMD ["./wait-for-it.sh", "rabbitmq-mgmt:5672", "--", "python", "enrollment.py"]
