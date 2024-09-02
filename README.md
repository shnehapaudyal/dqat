# Data Quality Assessment Tool (DQAT)

Data quality assessment tool provides simple yet powerful interfaces with features that help in data understanding and preprocessing stage. It includes both a backend and a frontend, with the backend built in Python and managed using `virtualenv`, and the frontend built with Node.js.

## Prerequisites

Ensure that you have the following installed on your system before proceeding:

- Python 3.x
- `virtualenv`
- Node.js
- npm (Node Package Manager)

## Setup

This command does the following:
- Creates a virtual environment in the venv directory.
- Installs all required Python packages listed in requirements.txt.
- Creates a touchfile to indicate that the environment setup is complete.

### 1. Build the Project
To set up both the Python environment and the Node.js dependencies in one step, you can run:

```bash
make build
```


### 2. Start the Frontend
To start the frontend of the application, run:

```bash
make client
```
This will navigate to the client directory and start the React development server silently.

### 3. Start the Backend
To start the backend of the application, run:

```bash
make server
```
This will activate the virtual environment and start the Python application by running main.py.