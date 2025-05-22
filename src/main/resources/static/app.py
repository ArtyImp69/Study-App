from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import fitz  # PyMuPDF
import docx
import pandas as pd
from PIL import Image
import shutil
import subprocess

app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

memory = []

def ask_ollama(model_name: str, prompt: str) -> str:
    command = ['ollama', 'run', model_name, '--prompt', prompt]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Errore Ollama: {result.stderr}")
    return result.stdout.strip()

@app.post("/api/process-file")
async def process_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    content = ""
    if file.filename.endswith(".pdf"):
        doc = fitz.open(file_path)
        content = "\n".join([page.get_text() for page in doc])
    elif file.filename.endswith(".docx"):
        doc = docx.Document(file_path)
        content = "\n".join([p.text for p in doc.paragraphs])
    elif file.filename.endswith(".csv"):
        df = pd.read_csv(file_path)
        content = df.to_string()
    elif file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        content = f"[IMAGE: {file.filename} salvata]"
    
    memory.append(content)
    return {"status": "success", "filename": file.filename, "content": content[:500]}

@app.post("/api/generate")
async def generate_response(prompt: str = Form(...)):
    combined_knowledge = "\n".join(memory)
    full_prompt = f"""Sei un assistente intelligente. Usa le seguenti informazioni per rispondere:

{combined_knowledge}

Domanda: {prompt}
Risposta:"""

    modello = "onicai/llama_cpp_canister_models"  # modifica con il modello che vuoi usare

    try:
        text = ask_ollama(modello, full_prompt)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    return JSONResponse(content={"answer": text})