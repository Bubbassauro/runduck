"""Start runduck app"""
import os
from runduck import app

if __name__ == "__main__":
    HOST = os.environ.get("SERVER_HOST", "localhost")
    try:
        PORT = int(os.environ.get("SERVER_PORT", "3825"))
    except ValueError:
        PORT = 3825
    app.run(host=HOST, port=PORT, threaded=True)
