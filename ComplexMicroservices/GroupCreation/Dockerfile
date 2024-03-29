FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./groupcreation.py .
COPY /SimpleMicroservices/log .env
COPY /SimpleMicroservices/notification .env2

RUN apt-get update && apt-get install -y wait-for-it

# Change the permissions of the wait-for-it.sh script
RUN chmod +x ./wait-for-it.sh

EXPOSE 5000

# Run app.py when the container launches
CMD ["./wait-for-it.sh", "rabbitmq-mgmt:5672", "--", "python", "./groupcreation.py"]
