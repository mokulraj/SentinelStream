from fastapi import FastAPI

app = FastAPI(title="SentinelStream")

@app.get("/")
def root():
    return {"message": "SentinelStream API Running"}
