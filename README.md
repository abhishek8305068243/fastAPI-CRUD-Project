FastAPI CRUD Application:-

This repository contains a full-stack CRUD application built to understand and demonstrate real-world backend and frontend development concepts.
The project focuses on building RESTful APIs using FastAPI, integrating a PostgreSQL database, and connecting it with a React-based frontend.

The goal of this project is to practice API design, database operations, frontend-backend communication, and Git/GitHub workflow in a structured and practical way.


🚀 What this project demonstrates

How to build REST APIs using FastAPI
How CRUD operations work in real applications
How to connect FastAPI with PostgreSQL using SQLAlchemy
How a React frontend communicates with backend APIs
How CORS works in a frontend-backend architecture
How to manage a full-stack project using Git & GitHub


✨ Features

Create, Read, Update, and Delete (CRUD) operations
RESTful API structure
PostgreSQL database integration
React-based frontend interface
CORS enabled for cross-origin requests
Clean and beginner-friendly project structure


🛠 Tech Stack

  Backend
    FastAPI (Python)
    SQLAlchemy
    PostgreSQL

  Frontend
    React
    JavaScript
    HTML
    CSS

  Tools & Version Control
    Git
    GitHub


    fastAPI-CRUD-Project/
│
├── main.py
├── models.py
├── database.py
├── database_models.py
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── .gitignore
└── README.md


Setup instructions:-

1️⃣ Clone the repository:-
git clone https://github.com/abhishek8305068243/fastAPI-CRUD-Project.git
cd fastAPI-CRUD-Project

2️⃣ Backend Setup:-
python -m venv myenv
myenv\Scripts\activate

Install backend dependencies: pip install fastapi uvicorn sqlalchemy psycopg2
Run the FastAPI server      : uvicorn main:app --reload
Backend will be available at: http://127.0.0.1:8000

3️⃣ Frontend Setup:-
cd frontend
npm install
npm start
Frontend will run at        : http://localhost:3000

🔗 API Endpoints (Examples):-
GET /products – Fetch all products
POST /products – Create a new product
PUT /products/{id} – Update an existing product
DELETE /products/{id} – Delete a product

🎯 Purpose of This Project:-

This project was built primarily for learning and hands-on practice, with a focus on:
Backend development using FastAPI
Database design and operations
Frontend and backend integration
Understanding real-world development workflow

📄 License:-
This project is licensed under the MIT License.
