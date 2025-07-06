
tmux kill-server

cd ~/greatness_portfolio || { echo "Project folder not found"; exit 1; }

git fetch
git reset --hard origin/main

# Activate virtual environment and install dependencies
source ~/greatness_portfolio/python3-virtualenv/bin/activate
pip install -r requirements.txt

# Start a new detached tmux session that runs the Flask server
tmux new-session -d -s flask_server "cd ~/greatness_portfolio && source venv/bin/activate && flask run --host=0.0.0.0"
