# app/task_manager.py

import os

class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.scripts = {}

    def add_script(self, name, content):
        self.scripts[name] = content
        os.makedirs("./scripts", exist_ok=True)
        with open(f"./scripts/{name}.py", "w") as f:
            f.write(content)

    def script_exists(self, name):
        return name in self.scripts

    def start_task(self, script_name):
        task_id = len(self.tasks) + 1
        self.tasks[task_id] = {"script": script_name, "status": "in_progress", "result": None}
        return task_id

    def get_task_status(self, task_id):
        if task_id not in self.tasks:
            return {"error": "Task not found"}
        return self.tasks[task_id]

    def update_task_status(self, task_id, status, result=None):
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = status
            self.tasks[task_id]["result"] = result
