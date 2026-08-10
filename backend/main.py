from fastapi import FastAPI

app = FastAPI()

@app.get("/main-commands")
async def get_all_commands():
    return {"message": "Hello World"}
