python setup.py sdist
pip install dist/*
rm -rf dist/
rm -rf *egg-info/
pip install -r requirements.txt
