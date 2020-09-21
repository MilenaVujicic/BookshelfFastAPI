import uvicorn
from config import PORT

if __name__ == "__main__":
    uvicorn.run("Bookshelf:app", host="localhost", port=int(PORT), reload=True, debug=True, workers=1)