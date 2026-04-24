# Simple Front-end and Back-end website running using Docker Containerization

The implementation is thanks to: [Docker Tutorial for Beginners](https://www.youtube.com/watch?v=b0HMimUb4f0)

## 📄 Overview
The project creates a compose stack of 4 services which ultimately creates a website with a MongoDB Database to store our data. The MongoDB data ensures our data is not lost when we turn off our service (persistence). The 4 services created are mysite-frontend, mysite-backend, mongo-express, mongo. Mongo-express allows us to connect, view and manage our MongoDB database from a browser instead of using the command line. We can browse data, edit data, manage collections, and run queries from the browser.


## 📋 Steps to reproduce
1. **Navigate to project location and run "docker compose build"** - This command will build our services (images) defined in the Docker-Compose.yaml.
'''bash
docker compose build
'''

2.  **If you need to install Docker**
    Download and install from: <https://docs.docker.com/get-started/introduction/get-docker-desktop/>


3. **Run "docker compose up"** - This will create and start our containers (instanstiations of our services or images).
'''bash
docker compose up
'''

4. **If you wish to develop on your local machine after cloning run:**
'''bash
python -m venv venv
venv\Scripts\activate
cd Backend
pip install -r requirements.txt
'''

## 🏗️ How to interact
- Navigate to **LocalHost:8081** on your web browser of choice to interact with the MongoDB database
- Navigate to **LocalHost:80** on your web browser of choice to input a value into the MongoDB Database
- Navigate to **LocalHost:8000/todos** to see list representation of values stored in MongoDB Dataabse
- Navigate to **LocalHost:8000/docs** to see the API or Swagger Docs

> [!NOTE]
The .env files are not currently included in the .gitignore file. The reasoning is to make the project replication as streamlined as possible. For a real-world appliaction you should always include .env files within your .gitignore.




