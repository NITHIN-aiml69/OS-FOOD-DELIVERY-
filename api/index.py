import os
import sys

# Ensure root directory is on the Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from platform_server import app

# Vercel WSGI entry point
# Exports 'app' for Vercel's Python runtime
if __name__ == "__main__":
    app.run(port=8080)
