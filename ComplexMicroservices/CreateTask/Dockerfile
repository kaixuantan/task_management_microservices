# Use the official Node.js image as the base image
FROM node:14-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY . /app

# Install the dependencies
RUN npm install
RUN apt-get update && apt-get install -y wait-for-it

# Change the permissions of the wait-for-it.sh script
RUN chmod +x ./wait-for-it.sh

# Expose the port on which your Node.js application will run
EXPOSE 5000

# Start the Node.js application
CMD ["./wait-for-it.sh", "rabbitmq-mgmt:5672", "--", "node", "create-task.js"]
