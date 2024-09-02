# Project Name

This project is a [brief description of your project]. It includes both a backend and a frontend, with the backend built in Python and managed using `virtualenv`, and the frontend built with Node.js.

## Prerequisites

Ensure that you have the following installed on your system before proceeding:

- Python 3.x
- `virtualenv`
- Node.js
- npm (Node Package Manager)

## Setup

Follow the steps below to set up the project environment:

### 1. Create and Activate a Virtual Environment

Run the following command to create and activate a Python virtual environment:

```bash
make venv
```

This command does the following:

- Creates a virtual environment in the venv directory.
- Installs all required Python packages listed in requirements.txt.
- Creates a touchfile to indicate that the environment setup is complete.

### 3. Build the Project
To set up both the Python environment and the Node.js dependencies in one step, you can run:

```bash
make build
```


### 4. Start the Frontend
To start the frontend of the application, run:

```bash
make client
```
This will navigate to the client directory and start the React development server silently.

### 5. Start the Backend
To start the backend of the application, run:

```bash
make server
```
This will activate the virtual environment and start the Python application by running main.py.