echo STARTUP backend
poetry run fastapi dev ./ws/main.py --host 0.0.0.0 --port 5001
