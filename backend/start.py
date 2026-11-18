"""Run the AttributeIQ FastAPI backend."""
import sys, os
import uvicorn

# Ensure backend directory is in path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

if __name__ == "__main__":
    uvicorn.run("main:app", app_dir=backend_dir, host="127.0.0.1", port=8000, reload=True, log_level="info")
