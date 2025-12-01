# Personal Data Sheet System in Django

PDS Management App made in Django, complete forms and id photo and digital signature. Can import to excel and pdf. Complete CRUD operations and has a separate admin panel for managing users


#### Sample page
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

### 5.) Create database
```bash
sudo mysql -u root

CREATE DATABASE pds_db DEFAULT CHARACTER SET utf8mb4;
CREATE USER 'pds_user'@'localhost' IDENTIFIED BY 'pds_password';
GRANT ALL PRIVILEGES on pds_db.* to 'pds_user'@'localhost';
FLUSH PRIVELEGES;
EXIT;

sudo systemctl start mysql
```

### 6.) Make Migrations and Migrate
```bash
python manage.py makemigrations pds_app
python manage.py migrate
```

### 7.) Create SuperUser first
```bash
python manage.py createsuperuser
```

### 8.) Run Server
```bash
python manage.py runserver
```

### 9. ) Open Localhost on web browser
```bash
http://127.0.0.1/
```

Goodluck : )