# 🚪 Portaria CTA — Access Management System 🚪

A simple access management system for visitors, delivery drivers, and ride-share drivers, built with **FastAPI (backend)** and **HTML + CSS + JavaScript (frontend)**. The database is managed with **PostgreSQL** via **Supabase**.

---

## 🚀 How to Run This Project

#### 🛠️ Installation Steps

1. Create and activate a virtual environment:

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac**

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

#### 🔧 Database Configuration

Edit `config/database.py` and set your database credentials:

```python
DATABASE_URL = "postgresql://user:password@localhost:5432/portaria"
```

#### 🚀 Run Database Migrations (Optional)

If using Alembic for migrations, execute:

```bash
alembic upgrade head
```

#### ▶️ Run the FastAPI Server:

```bash
uvicorn main:app --reload
```

Your API will be running at: [http://127.0.0.1:8000](http://127.0.0.1:8000)
Interactive documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 2️⃣ Frontend (HTML + CSS + JavaScript)

#### ⚙️ Requirements

* Any web browser (Chrome, Firefox, Edge, etc.)

#### 🛠️ Installation Steps

Navigate to the frontend directory:

```bash
cd front
```

#### ✅ Running the frontend:

**Option 1:** Using Python HTTP Server (recommended)

```bash
python -m http.server 5500
```

Open your browser at: [http://127.0.0.1:5500/front/home.html](http://127.0.0.1:5500/front/home.html)

**Option 2:** Using VSCode Live Server

* Install the VSCode extension **"Live Server"**.
* Right-click `index.html` → **"Open with Live Server"**.

---

## 🔗 API Main Endpoints

| Endpoint                | Method | Description              |
| ----------------------- | ------ | ------------------------ |
| `/auth/login`           | POST   | Authenticate a user      |
| `/auth/create_dweller`  | POST   | Create a new user        |
| `/order/request-access` | POST   | Submit an access request |

---

## ✔️ Important Notes:

* 🔐 The API uses JWT for authentication.
* ✅ The frontend saves JWT tokens in browser `localStorage`.
* 🌐 CORS is enabled for easy frontend communication.

Example CORS middleware setup (`main.py`):

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 💡 Project Features:

* Secure CPF + password-based authentication
* Home page
* Request access page (Uber, Delivery, Guest)
* Success confirmation page
* Admin notification (email or custom notifications)
* User logout functionality

---

## 🏆 Project by:

* 🚀 Academic Project — **Portaria CTA - IFSP**
