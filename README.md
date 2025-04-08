Installation steps
1. open termimal and type in "pip install uv"
2. after installing uv, inside the project folder type in "uv venv" (this will create a virtual environment)
3. type in "uv pip install -r requirements.txt"
4. inside the project folder create a file and name it .env and add your database details.
5. run the server using: uvicorn app.main:app --reload --port 8001 (or any port that is unoccupied)
