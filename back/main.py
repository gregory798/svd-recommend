import uvicorn
import functions as func
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Message": "Hello"}


@app.get("/recommend")
def recommend(algorithm_name: str, user_id: str):
    try:
        if algorithm_name == "svd":
            return func.svd(user_id)
    except Exception as e:
        return {"Error" : str(e)}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)