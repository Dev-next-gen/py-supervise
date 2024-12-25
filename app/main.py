from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.gpu_tasks import execute_gpu_task
from app.task_manager import TaskManager
from app.utils import monitor_resources
from app.monitoring import stream_monitoring
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

# Initialisation de l'application FastAPI
app = FastAPI(
    title="API GPU Management",
    description="API permettant la gestion des calculs GPU et le monitoring des ressources.",
    version="1.0.0",
)

# Configuration de CORS pour autoriser les connexions du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Autorise le frontend React
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes HTTP
    allow_headers=["*"],  # Permet tous les en-têtes HTTP
)

# Gestionnaire de tâches
task_manager = TaskManager()

# Modèles Pydantic
class Script(BaseModel):
    name: str
    content: str

class AnalysisRequest(BaseModel):
    results: str
    logs: str

class AnalysisResponse(BaseModel):
    advice: str

# Endpoint principal
@app.get("/")
def home():
    """
    Point d'entrée de l'API.
    """
    return {"message": "API pour calculs GPU opérationnelle"}

# Création de scripts
@app.post("/create_script/")
def create_script(script: Script):
    """
    Ajoute un script au gestionnaire de tâches.
    """
    if task_manager.script_exists(script.name):
        raise HTTPException(status_code=400, detail=f"Le script '{script.name}' existe déjà.")
    task_manager.add_script(script.name, script.content)
    return {"message": f"Script '{script.name}' ajouté avec succès."}

# Exécution de scripts
@app.post("/run_script/{script_name}")
def run_script(script_name: str, background_tasks: BackgroundTasks):
    """
    Exécute un script GPU en arrière-plan.
    """
    if not task_manager.script_exists(script_name):
        raise HTTPException(status_code=404, detail="Script non trouvé.")
    task_id = task_manager.start_task(script_name)
    background_tasks.add_task(execute_gpu_task, task_id, task_manager)
    return {"task_id": task_id, "status": "En cours"}

# Statut des tâches
@app.get("/task_status/{task_id}")
def get_task_status(task_id: int):
    """
    Récupère le statut d'une tâche en cours.
    """
    status = task_manager.get_task_status(task_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Tâche non trouvée.")
    return status

# Monitoring des ressources
@app.get("/resources")
def resources():
    """
    Renvoie les ressources GPU actuelles.
    """
    return monitor_resources()

# Streaming en temps réel des données de monitoring
@app.get("/monitoring")
def monitoring():
    """
    Monitoring en temps réel via Server-Sent Events (SSE).
    """
    return StreamingResponse(stream_monitoring(), media_type="text/event-stream")

# Endpoint pour l'analyse
@app.post("/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest):
    """
    Analyse les résultats et retourne des conseils.
    """
    advice = (
        f"Analyse des résultats : {request.results}\n"
        f"Logs fournis : {request.logs}\n\n"
        "Conseil : Tout semble fonctionner correctement. Continuez à surveiller les performances et à tester régulièrement."
    )
    return AnalysisResponse(advice=advice)
