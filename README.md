# ESD Project

Welcome to our Task and Project Management platform, a comprehensive solution designed to streamline your workflow. Our platform allows you to efficiently generate ideas, create groups, enroll members, and assign tasks, all in one place. With intuitive features and a user-friendly interface, managing your projects has never been easier. Stay organized, collaborate effectively, and achieve your project goals seamlessly.

## Quickstart

### Clone repository

1. Open your terminal.
2. Navigate to the directory where you want to clone the repository.
3. Run the command `git clone <repository-url>`. Replace `<repository-url>` with the URL of this repository.

### Start Frontend

1. Navigate to the frontend folder using the command `cd frontend`.
2. Install the necessary packages with `npm install`.
3. Start the development server with `npm run dev`.

### Start microservices

1. In the root folder, build the Docker images with `docker compose build`.
2. Start the Docker containers with `docker compose up`.

Your website is now live and can be accessed at http://localhost:5173. Enjoy browsing!

### Swagger API Documentation for Complex Microservices

Please note: This documentation is only accessible once the Docker containers are up and running.
| Complex Microservices          | Swagger Docs URL                           |
|-----------------|-------------------------------|
| Generate Ideas  | http://localhost:5000         |
| Group Creation  | http://localhost:5000/apidocs |
| Enrollment      | http://localhost:5002         |
| Create Tasks    | http://localhost:5003/api     |

### Use case Diagrams
https://drive.google.com/file/d/1PpDNxZTYQc-BbD_FvhH3TqepAS8cPTnp/view?usp=sharing