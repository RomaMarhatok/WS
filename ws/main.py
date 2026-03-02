import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def helth_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app")