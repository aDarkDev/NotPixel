@echo off

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

if not exist venv\Lib\site-packages\installed (
    if exist requirements.txt (
		echo installing wheel for faster installing
		pip install wheel
        echo Installing dependencies...
        pip install -r req.txt
        echo. > venv\Lib\site-packages\installed
    ) else (
        echo req.txt not found, skipping dependency installation.
    )
) else (
    echo Dependencies already installed, skipping installation.
)


echo Starting the bot...
python main.py

echo done
pause
