@echo off
echo === E-Commerce Setup ===

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements\dev.txt

REM Create .env file if not exists
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo Please update .env file with your configuration
)

REM Create necessary directories
echo Creating directories...
if not exist media\products mkdir media\products
if not exist media\categories mkdir media\categories
if not exist staticfiles mkdir staticfiles
if not exist logs mkdir logs

REM Run migrations
echo Running migrations...
python manage.py migrate

REM Create superuser
echo Creating superuser...
python manage.py createsuperuser

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

echo === Setup Complete ===
echo Run 'python manage.py runserver' to start the development server
pause
