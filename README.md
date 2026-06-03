# E-commerce
E-commerce site

## Quick start (Windows)

1. Open a terminal in the project root (ex-`c:\Users\Hp\Desktop\E-commerce`).

2. Create and activate a virtualenv (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

4. Apply migrations and run server (run from `djangopro` folder):
```powershell
cd djangopro
python manage.py migrate
python manage.py runserver
```

## Notes
- Required packages are listed in `requirements.txt` (Django, django-import-export, razorpay, Pillow).
- If you want exact pinned versions from your environment, I can generate them with `pip freeze > requirements.txt`.
