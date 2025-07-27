# 🍬 Sweet Shop Management System

A full-stack, user-friendly Sweet Shop Inventory and Purchase System built using **FastAPI**, **MongoDB**, and **React.js + CSS**. This project follows **Test-Driven Development (TDD)** principles, ensuring reliability and maintainability through rigorous testing using Python's `unittest` framework for both frontend and backend.

---

## ✨ Features Overview

| Feature         | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| ➕ Add Sweet     | Add new sweets with name, category, price, and quantity                    |
| ❌ Delete Sweet  | Delete a sweet (Admin only) from the database                              |
| 👁 View All      | Display all available sweets in a card layout                              |
| 🔍 Search        | Filter sweets by name, category, or price range                            |
| ⬆️ Update Sweet  | Update sweet details (price, quantity, etc.)                               |
| 🛒 Cart          | Add/remove sweets to/from cart, quantity adjustments with real-time sync   |
| 👤 Authentication | Users can log in/register to manage their cart                            |
| 🔐 Authorization | Only logged-in users can add/remove from cart                              |

---


## ⚙️ Technologies Used

### 🔧 Backend

- [Python 3](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [Pymongo](https://pymongo.readthedocs.io/)
- [Unittest](https://docs.python.org/3/library/unittest.html)

### 💻 Frontend

- [React.js](https://reactjs.org/)
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [Axios](https://axios-http.com/) for API calls

### 🛠 Development Tools

- [Postman](https://www.postman.com/) – API Testing
- [MongoDB Compass](https://www.mongodb.com/products/compass) – GUI for database
- [ChatGPT](https://chat.openai.com) – Debugging and suggestions

---

## ✅ Test-Driven Development (TDD)

We followed a strict TDD approach:

- All core features were written with **test-first** development.
- Backend tests written using **unittest**.
- Frontend interactions tested using **React Testing Library** (optional but recommended).

UI Overview
![App Screenshot](C:\Users\Admin\OneDrive\Pictures\Screenshots)



