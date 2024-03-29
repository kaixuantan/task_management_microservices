# Use an official Python runtime as a parent image
FROM python:3-slim

# Add the current directory contents into the container at /
WORKDIR /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y wait-for-it

# Change the permissions of the wait-for-it.sh script
RUN chmod +x ./wait-for-it.sh

EXPOSE 5000

# Run app.py when the container launches
CMD ["./wait-for-it.sh", "rabbitmq-mgmt:5672", "--", "python", "groupcreation.py"]