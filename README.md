# alx-project-nexus

# 🗳️ Online Poll System Backend – ProDev BE

This is the backend implementation of an **Online Poll System** developed as part of the **ProDev Backend Engineering Program**. The system enables real-time voting functionality with optimized database design, scalable APIs, and thorough API documentation.

## 📚 ProDev Backend Engineering Program Overview

This program focused on practical backend development skills using industry-standard tools and patterns. Through real-world projects like this online poll system, we explored:

### 🔑 Key Technologies Covered
- **Python** – Core language for backend logic
- **Django** – Robust framework for rapid API development
- **REST APIs** – For client-server communication
- **GraphQL** – Alternative data querying (explored in related projects)
- **Docker** – For containerization and environment consistency
- **CI/CD** – Automated build, test, and deployment pipelines

### 🧠 Important Backend Concepts
- **Database Design** – Normalization, relationships, indexing
- **Asynchronous Programming** – Background tasks & real-time behavior
- **Caching Strategies** – Optimizing read performance and scalability

---

## 📌 Project Overview

This case study simulates a backend for a real-time voting platform. Users can create polls, vote, and see results immediately. The backend is built for performance, reliability, and developer usability.

### 🎯 Project Goals
- ✅ Build REST APIs for poll creation, voting, and result retrieval
- ✅ Design efficient PostgreSQL schemas
- ✅ Host Swagger documentation at `/api/docs`

---

## ⚙️ Technologies Used
- **Django** – API development & ORM
- **PostgreSQL** – Relational database for polls and votes
- **Swagger / drf-yasg** – Auto-generated API documentation
- **Docker** – For containerized development and deployment

---

## 🔑 Key Features

### 1. 🗳️ Poll Management
- Create polls with multiple options
- Attach metadata: title, creation date, expiry

### 2. 👤 Voting System
- Cast votes via secure endpoints
- Prevent duplicate votes using user/session constraints

### 3. 📊 Real-Time Results
- Get live vote counts for each poll
- Efficient aggregation queries for scalability

### 4. 📄 API Documentation
- Swagger docs generated with `drf-yasg`
- Access via `/api/docs` route

### 5. 📄 Project demo link
- [project demo](https://alx-project-nexus-production-acc9.up.railway.app/api/docs/)
