import os
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from faster_whisper import WhisperModel

app = FastAPI(title="Local Whisper API")

# Configuration
MODEL_SIZE = os.getenv("WHISPER_MODEL", "large-v3-turbo")
DEVICE = os.getenv("WHISPER_DEVICE", "cpu")  # "cuda" or "cpu"
COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8") # "float16", "int8", etc.

print(f"Loading Whisper model '{MODEL_SIZE}' on {DEVICE} ({COMPUTE_TYPE})...")
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

@app.get("/v1/models")
async def list_models():
    return {
        "data": [
            {
                "id": "whisper-1",
                "object": "model",
                "owned_by": "local",
                "permission": []
            }
        ]
    }

@app.post("/v1/audio/transcriptions")
async def transcribe(
    file: UploadFile = File(...),
    model_name: str = Form("whisper-1", alias="model"),
    language: str = Form(None),
    prompt: str = Form(None),
    response_format: str = Form("json"),
    temperature: float = Form(0.0),
):
    # Save uploaded file to a temporary location
    suffix = os.path.splitext(file.filename)[1] if file.filename else ".tmp"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        segments, info = model.transcribe(
            tmp_path,
            language=language,
            initial_prompt=prompt,
            temperature=temperature,
            beam_size=5,
        )
        
        # Combine segments into a single string
        text = "".join([segment.text for segment in segments]).strip()
        
        if response_format == "text":
            return text
        
        return {"text": text}
    except Exception as e:
        print(f"Error during transcription: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("WHISPER_PORT", 9000))
    uvicorn.run(app, host="0.0.0.0", port=port)
