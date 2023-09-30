# U-Projects
This repository contains a dockerized setup for running U-Projects. With Docker, you can easily set up and run the application without worrying about environment configuration.
## Prerequisites
Before you begin, ensure you have the following tools installed on your system:
- [Docker](https://docker.com/get-started)
- [Python](https://python.org/downloads)@3.10.12
- [Node.js](https://nodejs.org/)@16.13.2
## Get Started
Follow these steps to clone and run U-Projects using Docker:
1. **Clone the Repository**
    ```bash
    git clone https://github.com/andrewBurrr/uprojects.git
    ```
2. **Create a Virtual Environment for Python**
   This will help encapsulate any dependencies, and ensure that the projects requirements are as slim as possible
    ```bash
    # Create a virtual environment
    python -m venv venv
        
    # Activate the virtual environment (Windows)
    venv\Scripts\activate
       
    # Activate the virtual environment (macOS/Linux)
    source venv/bin/activate  
    ```
3. **Build and Run the Docker Containers**
    To build and run the containers, we use the following command:
    ```bash
    docker-compose up -d --build
    ```
4. **Access the Application**
    Once the containers are running, you can access the application in your web browser at `http://localhost:3000`
5. **Stop and Clean Up**
    To stop the application and remove the containers run:
    ```bash
    docker-compose down
    ```

## Installing Dependencies
If your development work on this application requires you to add any dependencies for the backend application, ensure that you add them to the ```requirements.txt``` file before running your program. This can be done by running the following command in the same directory as the ```manage.py```:
```bash
    pip freeze > requirements.txt
```
Any dependencies pertaining to the frontend application should be added to the ```package.json``` file which is automatic as long as you don't specify the devDependency flag ```--save-dev``` or ```-D```