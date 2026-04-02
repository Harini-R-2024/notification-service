# 🏗 Notification Service - Design Document

## 📌 Overview

This document describes the architecture, design decisions, and scalability considerations for the Notification Service.

The system is designed to handle **high throughput, reliability, and asynchronous processing**.

---

## 🧱 High-Level Architecture

```
Client → FastAPI → Database → Queue → Worker → Notification Delivery
```

### Flow Explanation:

1. Client sends notification request
2. API stores notification in database
3. Notification is pushed to queue
4. Background worker processes queue
5. Notification is sent (simulated)

---

## 🗄 Database Design

### 1. Notifications Table

| Column     | Type     | Description           |
| ---------- | -------- | --------------------- |
| id         | Integer  | Primary key           |
| user_id    | String   | User identifier       |
| message    | String   | Notification content  |
| priority   | String   | Notification priority |
| status     | String   | pending/sent/failed   |
| created_at | DateTime | Timestamp             |

---

### 2. User Preferences Table

| Column        | Type    | Description      |
| ------------- | ------- | ---------------- |
| id            | Integer | Primary key      |
| user_id       | String  | Unique user      |
| email_enabled | Boolean | Email preference |
| sms_enabled   | Boolean | SMS preference   |
| push_enabled  | Boolean | Push preference  |

---

### 3. Notification Logs (Conceptual)

| Column          | Type    | Description    |
| --------------- | ------- | -------------- |
| id              | Integer | Primary key    |
| notification_id | Integer | Reference      |
| channel         | String  | email/sms/push |
| status          | String  | sent/failed    |
| retry_count     | Integer | Retry attempts |

---

## 🔄 Queue Design

* Used **Priority Queue**
* Lower number = higher priority
* Handles:

  * critical
  * high
  * normal
  * low

---

## 🔁 Retry Mechanism

* Max retries: **3**
* Exponential backoff:

  * 1st → 2 sec
  * 2nd → 4 sec
  * 3rd → 8 sec
* Prevents system overload

---

## ⚡ Scalability Considerations

### Current (Demo)

* In-memory queue
* Single worker thread

### Production Improvements

* Replace with Redis / RabbitMQ
* Multiple worker instances
* Horizontal scaling
* Load balancing

---

## 🛡 Reliability

* Notifications stored in DB before processing
* Queue ensures async processing
* Retry mechanism handles failures

---

## 🔐 Idempotency (Future Scope)

* Can use unique request ID
* Prevent duplicate notifications

---

## 📊 Observability

* Logging added for:

  * Processing
  * Failures
  * Retries

---

## ⚖️ Trade-offs

| Decision        | Trade-off                       |
| --------------- | ------------------------------- |
| SQLite          | Easy setup but not scalable     |
| In-memory queue | Simple but not persistent       |
| Thread worker   | Lightweight but limited scaling |

---

## 🚀 Future Enhancements

* Redis queue integration
* Real email/SMS providers
* Rate limiting per user
* Analytics dashboard
* Webhook support

---

## 💡 Conclusion

The system demonstrates:

* Scalable architecture
* Async processing
* Fault tolerance
* Clean API design

It can be easily extended to production-grade systems.
