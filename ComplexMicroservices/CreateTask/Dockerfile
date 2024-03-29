# Use the official Node.js image as the base image
FROM node:14-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the wait-for-it.sh script from the host to the container
# COPY wait-for-it.sh ./

# Copy the rest of the application code to the container
COPY . .

# Expose the port on which your Node.js application will run
EXPOSE 5000

# Start the Node.js application
CMD ["node", "create-task.js"]
