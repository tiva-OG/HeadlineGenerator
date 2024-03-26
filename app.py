import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from headlineGenerator.pipeline.prediction import PredictionPipeline

text: str = "What is Text Summarization"

app = FastAPI()


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train():
    try:
        os.system("python main.py")
        return Response("Training successful!!!")
    except Exception as e:
        return Response(f"Error Occurred {e}")


@app.post("/predict")
async def predict(text):
    try:
        pipe = PredictionPipeline()
        text = pipe.predict(text)
        return text
    except Exception as e:
        raise e


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
