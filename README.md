# 🚀 Notification Service (Backend)

## 📌 Project Overview

This project is a **scalable Notification Service** built using FastAPI.
It supports sending notifications via multiple channels (Email, SMS, Push) with priority handling, retry mechanisms, and user preferences.

The system is designed to handle **high throughput and reliability** using asynchronous processing with a queue-based architecture.

---

## 🛠 Tech Stack

* **Backend Framework:** FastAPI
* **Language:** Python
* **Database:** SQLite (for demo)
* **ORM:** SQLAlchemy
* **Queue:** In-memory Priority Queue
* **Worker:** Background thread
* **Validation:** Pydantic

---

## ⚙️ Features Implemented

### ✅ Core Features

* Send notifications via API
* Multi-channel support (Email, SMS, Push - structure ready)
* User preferences (opt-in / opt-out)
* Priority handling (critical, high, normal, low)
* Notification status tracking (basic)

---

### 🚀 Advanced Features

* Asynchronous processing using queue
* Background worker for notification processing
* Retry mechanism (max 3 retries)
* Exponential backoff strategy
* Priority-based processing

---

## 📡 API Endpoints

### 🔹 Notifications

* `POST /notifications` → Create notification
* `GET /notifications/{id}` → Get notification by ID
* `GET /users/{user_id}/notifications` → Get user notifications

---

### 🔹 User Preferences

* `POST /users/{user_id}/preferences` → Set preferences
* `GET /users/{user_id}/preferences` → Get preferences

---

## ▶️ How to Run Locally

### 1. Clone repository

```bash
git clone <your-repo-link>
cd notification-service
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run server

```bash
python -m uvicorn app.main:app --reload
```

---

## 🌐 API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Example Request

```json
POST /notifications

{
  "user_id": "123",
  "message": "Hello Harini",
  "channels": ["email", "sms"],
  "priority": "high"
}
```

---

## 🔁 Retry Mechanism

* Retries failed notifications up to **3 times**
* Uses **exponential backoff**:

  * 1st retry → 2 seconds
  * 2nd retry → 4 seconds
  * 3rd retry → 8 seconds

---

## 📊 System Flow

```
Client → API → Database → Queue → Worker → Notification Processing
```

---

## ⚠️ Assumptions

* External services (Email/SMS) are mocked
* Authentication is not implemented
* SQLite used for simplicity (can be replaced with PostgreSQL)

---

## 🚀 Future Improvements

* Integrate Redis/RabbitMQ
* Add real email/SMS providers
* Add authentication & authorization
* Add analytics dashboard
* Add webhook support

---

## 👩‍💻 Author

Harini Radhakrishnan
