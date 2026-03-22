# 🎬 FastAPI Movie Ticket Booking System

## 🚀 Overview

This project is a fully functional backend application built using **FastAPI** that simulates a real-world movie ticket booking system.

It allows users to browse movies, book tickets, manage seat availability, and perform advanced operations such as search, filtering, sorting, and pagination.

---

## 🛠️ Tech Stack

* **FastAPI** – Modern Python web framework
* **Python** – Core programming language
* **Pydantic** – Data validation
* **Uvicorn** – ASGI server

---

## ✨ Features

### 🎯 Movie Management

* View all movies
* Get movie details by ID
* Movie summary analytics
* Add new movies
* Update movie details
* Delete movies (with validation rules)

---

### 🎟️ Booking System

* Create bookings with validation
* Automatic ticket price calculation
* Promo code support (SAVE10, SAVE20)
* Track total bookings and revenue

---

### 🔄 Seat Workflow System

* Hold seats temporarily
* Confirm bookings from holds
* Release held seats
* Prevent overbooking

---

### 🔍 Advanced Features

* **Search** movies (title, genre, language)
* **Filter** movies with multiple conditions
* **Sort** movies dynamically
* **Pagination** support
* **Combined Browse API** (search + filter + sort + pagination)

---

## 📡 API Endpoints

### 🎬 Movies

* `GET /movies`
* `GET /movies/{movie_id}`
* `GET /movies/summary`
* `GET /movies/filter`
* `GET /movies/search`
* `GET /movies/sort`
* `GET /movies/page`
* `GET /movies/browse`

---

### 🎟️ Bookings

* `POST /bookings`
* `GET /bookings`
* `GET /bookings/search`
* `GET /bookings/sort`
* `GET /bookings/page`

---

### 🔄 Seat Workflow

* `POST /seat-hold`
* `GET /seat-hold`
* `POST /seat-confirm/{hold_id}`
* `DELETE /seat-release/{hold_id}`

---

## 🧪 API Testing

All APIs are tested using Swagger UI:

👉 http://127.0.0.1:8000/docs

Screenshots of all endpoints are available in the `screenshots/` folder.

---

## 📁 Project Structure

```
fastapi-movie-ticket-booking/
│
├── main.py
├── requirements.txt
├── README.md
└── screenshots/
```

---

## ▶️ How to Run

### 1️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 2️⃣ Run server

```
uvicorn main:app --reload
```

### 3️⃣ Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 🧠 Concepts Covered

* REST API design
* Pydantic validation
* Helper functions
* CRUD operations
* Multi-step workflow
* Search, sorting, pagination

---

## 💼 Real-World Use Case

This project represents backend systems used in:

* Movie ticket booking platforms
* Reservation systems
* Online service platforms

---

## 👨‍💻 Author

FastAPI Internship Final Project

---

## 🌟 Highlights

* Clean and structured code
* End-to-end workflow implementation
* Fully tested APIs
* Covers beginner to advanced concepts

---
