# PySupervise

PySupervise is a lightweight backend built with FastAPI for real-time task monitoring and resource tracking. It features Server-Sent Events (SSE) to provide live updates on CPU, memory, and GPU usage, along with task execution and status monitoring.

---

## Features

- **Real-time Monitoring:** Live updates on system resources.
- **Task Management:** Submit, execute, and monitor long-running tasks.
- **RESTful API:** Intuitive endpoints for integration.
- **Lightweight Backend:** Built with FastAPI for speed and simplicity.

---

## Prerequisites

- **Python 3.7**  
  Make sure you have Python 3.7 installed on your system.  
  If needed, download it from [Python's official website](https://www.python.org/downloads/).

- **Virtual Environment (tensorflow_env):**  
  Use an isolated virtual environment to manage dependencies.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/py-supervise.git
   cd py-supervise

Activate your virtual environment:

C:\Windows\System32\tensorflow_env\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the application:

uvicorn app.main:app --reload

Access the API documentation at:
http://127.0.0.1:8000/docs

---

## Testing

To run tests, activate your virtual environment and execute:

pytest


License

This project is licensed under the MIT License. See the LICENSE file for details.

fastapi==0.78.0
uvicorn==0.17.0
psutil==5.9.0
