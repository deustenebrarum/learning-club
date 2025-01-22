python -m venv venv
call "venv/Scripts/activate"

pip install -r requirements.txt

python scripts/generate_env.py
