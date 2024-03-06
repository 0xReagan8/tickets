import uvicorn
from app import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8181)
    # uvicorn.run(app, host="192.168.0.15", port=5800)