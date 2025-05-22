from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import fitz  # PyMuPDF
import docx
import pandas as pd
from PIL import Image
import shutil
from llama_cpp import Llama

# Carica il modello al primo avvio
llm = Llama(model_path="models/mistral-7b-instruct.Q4_K_M.gguf", n_ctx=2048, n_threads=8)
app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

memory = []  # Questa sarà la "memoria" dell’AI per ora

@app.post("/api/process-file")
async def process_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Salva il file
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
        image = Image.open(file_path)
        content = f"[IMAGE: {file.filename} salvata]"

    memory.append(content)  # Salva il contenuto nella memoria

    return {"status": "success", "filename": file.filename, "content": content[:500]}  # Limita la risposta


@app.post("/api/generate")
async def generate_response(prompt: str = Form(...)):
    combined_knowledge = "\n".join(memory)

    full_prompt = f"""Sei un assistente intelligente. Usa le seguenti informazioni per rispondere:

{combined_knowledge}

Domanda: {prompt}
Risposta:"""

    response = llm(full_prompt, max_tokens=512, stop=["Domanda:"], echo=False)
    text = response["choices"][0]["text"].strip()

    return JSONResponse(content={"answer": text})
