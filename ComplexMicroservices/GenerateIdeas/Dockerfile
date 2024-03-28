# Use an official Python runtime as a parent image
FROM python:3-slim

COPY ./requirements.txt ./
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Add the current directory contents into the container at /
COPY generate_ideas.py ./
COPY get_pdf.py ./
COPY get_users_email.py ./
COPY process_pdf.py ./
COPY send_amqp.py ./
COPY .env ./

# Run app.py when the container launches
CMD ["python", "generate_ideas.py"]