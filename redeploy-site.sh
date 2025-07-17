cd mlh-portfolio
git fetch
git reset origin/main --hard

python3 -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt
deactivate

systemctl daemon-reload
systemctl restart myportfolio