# Social Network API

This is a REST API for a social network application built with Django and Django Rest Framework. It provides endpoints for user registration, authentication, and user search functionality.

## Getting Started

### Prerequisites

- Docker

### Clone the Repository

1. Clone this repository to your local machine using:
`git clone https://github.com/Roboid537/social_network.git`

2. Navigate to the project directory: `cd social_network`


### Configure Environment Variables

3. Create a `.env` file in the project root directory and set the following environment variables:
```
SECRET_KEY=""
DATABASE_NAME=""
DB_USER=""
DB_PASSWORD=""
DB_HOST=""
DB_PORT=""
```


### Create Database

3. Create a PostgreSQL database for the application. Update the database credentials in the `.env` file:

```
DATABASE_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_database_host
DB_PORT=your_database_port
```

### Build and Run the Application

4. Build the Docker image using the Dockerfile:
`docker build -t social_network .`


5. Run the Docker container: `docker run -p 8000:8000 --env-file .env social_network`


### API Testing
6. Import collection 'Social Network.postman_collection.json' in postman and test apis.