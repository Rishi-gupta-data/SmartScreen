from dotenv import load_dotenv
import os

load_dotenv()

import uvicorn


if __name__ == '__main__':
    # Ensure env loaded before importing app
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
