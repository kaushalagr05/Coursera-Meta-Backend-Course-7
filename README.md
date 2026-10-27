# Little Lemon Restaurant Booking System
**Meta Back-End Developer Specialization — Course 7: The Full Stack**

This repository contains the complete implementation of the **Little Lemon Booking System** satisfying all 13 Coursera peer-review grading rubric criteria.

---

## 📋 Rubric Compliance & Verification Checklist

| # | Rubric Item | Implementation Location | Status |
|---|-------------|-------------------------|--------|
| **1** | `restaurant` registered in `INSTALLED_APPS` | `littlelemon/settings.py` | ✅ Verified |
| **2** | MySQL database configuration (`'ENGINE': 'django.db.backends.mysql'`, DB: `'littlelemon'`, user: `'root'`, host: `'127.0.0.1'`, port: `'3306'`) | `littlelemon/settings.py` | ✅ Verified |
| **3** | `Booking` model with `first_name`, `reservation_date`, `reservation_slot` and `__str__` method | `restaurant/models.py` | ✅ Verified |
| **4** | Initial migrations generated | `restaurant/migrations/0001_initial.py` | ✅ Verified |
| **5** | Route `/book/` renders `restaurant/templates/book.html` | `restaurant/views.py`, `restaurant/urls.py` | ✅ Verified |
| **6** | Route `/reservations/` passes serialized JSON (`serializers.serialize('json', Booking.objects.all())`) to `reservations.html` | `restaurant/views.py`, `restaurant/urls.py` | ✅ Verified |
| **7** | Route `/bookings` handles **GET** with optional `?date=YYYY-MM-DD` (defaults to today's date) returning serialized JSON | `restaurant/views.py` | ✅ Verified |
| **8** | Route `/bookings` handles **POST** with JSON payload (`json.loads(request.body)`), checking duplicates and returning 400 or saving record with 200/201 | `restaurant/views.py` | ✅ Verified |
| **9** | URL configurations in `restaurant/urls.py` and `littlelemon/urls.py` | `restaurant/urls.py`, `littlelemon/urls.py` | ✅ Verified |
| **10** | `book.html` input fields: `first_name`, date picker `reservation_date` (`type="date"`), dropdown `reservation_slot` | `restaurant/templates/book.html` | ✅ Verified |
| **11** | JavaScript initializes `reservation_date` with today's date on `DOMContentLoaded` and triggers `getBookings()` | `restaurant/templates/book.html` | ✅ Verified |
| **12** | JavaScript `change` event listener on `reservation_date` calls `getBookings()`, marks reserved slots disabled/gray, updates `#bookings`, or shows `"No Booking"` | `restaurant/templates/book.html` | ✅ Verified |
| **13** | JavaScript form submission uses vanilla `fetch('/bookings', { method: 'POST', ... })` with CSRF header, then re-fetches bookings; `reservations.html` displays raw JSON inside `<pre>` tag | `restaurant/templates/book.html`, `restaurant/templates/reservations.html` | ✅ Verified |

---

## 🚀 Setup & Execution Guide

### 1. Prerequisites
- Python 3.10+ (or 3.11/3.12/3.13/3.14)
- MySQL Server running on `127.0.0.1:3306` with database `littlelemon`

### 2. Setting Up Virtual Environment via Pipenv

```bash
# Install pipenv if not already installed
pip install pipenv

# Install project dependencies
pipenv install

# Activate the virtual environment
pipenv shell
```

*(Alternatively, standard venv: `python -m venv venv; source venv/bin/activate` or `venv\Scripts\activate; pip install -r requirements.txt`)*

### 3. Database Setup & Migrations

In MySQL shell or client:
```sql
CREATE DATABASE IF NOT EXISTS littlelemon;
```

Run Django migrations:
```bash
python manage.py makemigrations restaurant
python manage.py migrate
```

### 4. Running the Development Server

```bash
python manage.py runserver
```

Open your browser to:
- **Home:** `http://127.0.0.1:8000/`
- **Book a Table:** `http://127.0.0.1:8000/book/`
- **Reservations (Rubric Review):** `http://127.0.0.1:8000/reservations/`
- **Bookings API:** `http://127.0.0.1:8000/bookings`

### 5. Running Automated Unit Tests

```bash
python manage.py test
```

---

## 📦 Packaging for Coursera Submission

To create a clean zip archive excluding caches, virtual environments, and SQLite local test files:

### Windows (PowerShell):
```powershell
Compress-Archive -Path littlelemon, restaurant, manage.py, Pipfile, Pipfile.lock, requirements.txt, README.md -DestinationPath littlelemon_project.zip -Force
```

### macOS / Linux (Terminal):
```bash
zip -r littlelemon_project.zip . -x "*.git*" "*__pycache__*" "*.pyc" "*db.sqlite3" "*venv*" "*.venv*"
```
