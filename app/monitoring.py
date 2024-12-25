from fastapi.responses import StreamingResponse
import time
import json
from app.utils import monitor_resources
from app.task_manager import TaskManager

task_manager = TaskManager()

def stream_monitoring():
    """
    Génère les données de monitoring en temps réel.
    """
    while True:
        # Récupérer l'état des ressources
        resources = monitor_resources()

        # Récupérer l'état des tâches
        tasks = [
            {"task_id": task_id, "status": task["status"], "result": task["result"]}
            for task_id, task in task_manager.tasks.items()
        ]

        # Préparer les données à transmettre
        data = {
            "resources": resources,
            "tasks": tasks,
            "timestamp": time.time()
        }

        # Envoyer les données sous forme JSON
        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(1)  # Intervalle de 1 seconde entre chaque mise à jour
