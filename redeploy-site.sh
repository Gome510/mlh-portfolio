tmux kill-server

cd mlh-portfolio
git fetch
git reset origin/main --hard

python3 -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt
deactivate

tmux new-session -d -s server "cd ~/mlh-portfolio && source python3-virtualenv/bin/activate && flask run --host=0.0.0.0"