import os
import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class LlamaEngineSingleton:
    engine_instance = None

    @classmethod
    def get_instance(cls):
        from engine_llama_cpp import LlamaCPPEngine
        if cls.engine_engine_instance is None:
            cls.engine_instance = LlamaCPPEngine(
                repo_id="microsoft/Phi-3-mini-4k-instruct-gguf",
                filename="*q4.gguf",
                n_ctx=4096,
                n_threads=8,
                verbose=False
            )
        return cls.engine_instance


class Query(BaseModel):
    context: str
    question: str


@app.post("/generate-response/")
async def generate_response(query: Query):
    engine = LlamaEngineSingleton.get_instance()
    try:
        response = engine.generate_response(context=query.context, question=query.question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def read_root():
    pid = os.getpid()
    return {"message": f"Hello from Agent {pid}"}


if __name__ == "__main__":
    port = int(os.environ.get("AGENT_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
