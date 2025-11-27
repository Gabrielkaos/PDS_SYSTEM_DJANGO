# Personal Data Sheet System in Django
![alt text](https://github.com/Gabrielkaos/PDS_SYSTEM_DJANGO/blob/main/page.png?raw=true)

## Installing and Running
### 1.) Create virtual environment

Linux/Mac/Windows
```bash
python -m venv .venv
```
### 2.) Activate
Linux/Mac
```bash
source .venv/bin/activate
```
Windows
```bash
.venv\Scripts\Activate.ps1
```

### 3.) Installing modules
```bash
pip install -r requirements.txt
```

### 4.) Create media
```bash
mkdir -p media/id_photos
```

### 5.) Make Migrations and Migrate
```bash
python manage.py makemigrations pds_app
python manage.py migrate
```

### 5.) Run Server
```bash
python manage.py runserver
```

### 7. ) Open Localhost on web browser
```bash
http://127.0.0.1/
```

Goodluck : )