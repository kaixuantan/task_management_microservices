FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./groupcreation.py .
COPY /SimpleMicroservices/log .env
COPY /SimpleMicroservices/notification .env2
CMD [ "python", "./groupcreation.py" ]