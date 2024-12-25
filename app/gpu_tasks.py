# app/gpu_tasks.py

import subprocess
from app.task_manager import TaskManager

def execute_gpu_task(task_id, task_manager: TaskManager):
    task = task_manager.tasks[task_id]
    script_name = task["script"]
    script_path = f"./scripts/{script_name}.py"

    try:
        # Exécuter le script
        result = subprocess.check_output(["python", script_path], stderr=subprocess.STDOUT)
        task_manager.update_task_status(task_id, "completed", result.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        task_manager.update_task_status(task_id, "error", e.output.decode("utf-8"))
