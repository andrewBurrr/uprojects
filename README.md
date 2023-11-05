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
    It is possible that testing environments will start a new db volume on each run. As a result, you may want to run:
    ```bash
    docker exec -it uprojects_django python manage.py createsuperuser
    ```
    This should give you at least a single user for testing purposes. We are working on an alternative solution that gives a shared db that is pre-filled with testing data.
4. **Access the Application**
    Once the containers are running, you can access the frontend react application in your web browser at `http://localhost:3000`, and the backend api will be located at `http://localhost:8000`
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

## Testing
Use the included `docker-compose.test.yml` in order to test the application in a production like environment. THis command can be run with:
```bash
    docker-compose -f docker-compose.test.yml up -d --build
```
# Additional Developer Notes
Below is included details and policies about the development of this project, in order to assist developers in maintaining clean code, and increase the ease of development.
## React Project structure
The directory structure of this project is listed below:
1. `apis`:
    This directory contains objects and structures used to connect to backend api services
2. `assets`:
    This directory contains static files and assets used for rendering the frontend (i.e. pictures, markdown, etc.)
3. `components`:
    This directory contains components that are shared between multiple pages in the application (i.e. the same button is used on every page)
4. `contexts`:
    This directory contains components that provide context environments to other components (i.e. global variables)
5. `helpers`:
    This directory contains miscellaneous functions and helper objects that asist other components, but don't fit anywhere nicely
6. `hooks`:
    This directory contains react hooks that are used by more than one component
7. `layouts`:
    This directory contains page layout components so multiple pages can inherit the same formatting
8. `styles`:
    This directory contains custom styles and/or material themes that are shared between components
9. `types`:
    This directory defines types that are shared across components (i.e. defined types for the expected api objects)
10. `views`:
    This directory will have subdirectories that define each page of the application. These subdirectories should contain any single use components and a primary page component that can be routed to by react router
## Updates to Models (Backend)
When any of the models.py files are updated:
1. Clean-up:
    Delete the `*/uprojects/backend/db.sqlite3` file
2. Re-make all migrations:
    Navigate to `*/uprojects/backend/`
    If you have not made migrations before execute:
    ```bash
    python manage.py makemigrations users
    python manage.py makemigrations projects
    python manage.py migrate users
    python manage.py migrate projects
    ```
    If you have made migrations for both users and projects before execute:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
3. Run
    If you need the forntend running, follow the instructions for building and running the docker containers.
    If you only need the backend running, execute:
    ```bash
    python manage.py runserver
    ```