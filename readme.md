# 🌾 AI-Driven Wheat Yield Prediction & Crop Management System

## 🚀 Overview

This project leverages **Machine Learning** and **AI-driven insights** to help farmers and agricultural stakeholders predict wheat crop yields and make data-informed decisions for effective **crop management**. The backend is built using **FastAPI** with a modular features-based architecture, fully integrated with **PostgreSQL**, supporting secure authentication and future extensibility.

---

## 🔍 Key Features

- ✅ **User Authentication System** (Signup/Login) with hashed passwords
- 🧠 **AI-Powered Yield Prediction**
- 🌱 **Crop Management Recommendations** based on environmental & soil data
- 📦 **PostgreSQL** with SQLAlchemy for robust and scalable data storage
- ⚡ **Asynchronous APIs** using FastAPI for high performance
- 🧩 **Modular Codebase** using a feature-based folder structure
- 🌐 **Interactive API docs** via Swagger (`/docs`)

---

## 🛠️ Tech Stack

| Tech             | Usage                                      |
|------------------|---------------------------------------------|
| **FastAPI**      | Web API framework (asynchronous, fast)      |
| **SQLAlchemy**   | ORM for DB interactions                     |
| **PostgreSQL**   | Relational database                         |
| **asyncpg**      | High-performance async Postgres driver      |
| **Pydantic v2**  | Data validation and serialization           |
| **Passlib**      | Secure password hashing                     |
| **Python 3.11+** | Backend language                            |

---

## 📁 Project Structure (Feature-Based)

```
Backend/
├── main.py
├── .env
├── core/
│   ├── config.py
│   └── db.py
├── api/
│   └── routes.py
├── features/
│   └── auth/
│       ├── routes.py
│       ├── schemas.py
│       ├── services.py
│       ├── validators.py
│       └── models.py
└── requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://<username>:<password>@localhost:5432/<database_name>
API_KEY=your_api_key_here
```

---

## 🚀 Getting Started

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

#### On Windows:
```bash
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the FastAPI app on 0.0.0.0 (accessible over the network)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

> 🟢 Your app will now be available at:
> - Swagger UI: `http://localhost:8000/docs` on your machine
> - Network access: `http://<your-local-ip>:8000/docs` from other devices

---

## 🧑‍💻 Contributing

We welcome contributions! Feel free to fork the repo, create a new branch, and submit a PR. Please ensure your code is well-documented and tested.