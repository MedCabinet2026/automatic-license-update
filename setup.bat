@echo off

echo Creating virtual environment...

python -m venv .venv

call .venv\Scripts\activate

echo Installing packages...

python -m pip install --upgrade pip

pip install -r requirements.txt

echo Installation complete.

pause