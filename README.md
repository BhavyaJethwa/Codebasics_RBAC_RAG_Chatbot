# 🛡️ Codebasics RBAC + RAG Chatbot

A secure, role-based access control (RBAC) chatbot system using Retrieval-Augmented Generation (RAG) for personalized responses, built with **FastAPI** and **Streamlit**. This project enables department-specific document search and chat functionality with robust authentication and authorization.

## 📌 Features

- 🔐 **User Authentication**: Login and password management
- 👥 **Role-Based Access Control**:
  - Admins can add users, roles, and upload documents
  - Normal users can only chat and query documents as per their role and access.
- 🧠 **RAG-Powered Chatbot**:
  - Answers questions using uploaded documents
  - Role-specific response filtering
- 📄 **Document Upload**: Supports uploading any type of files per role
- 📜 **Chat History**: Stores session-wise history
- 🔄 **Password Reset**: Secure reset functionality
- 📊 **Admin Dashboard**: View roles, users, and logs

## 🏗️ Tech Stack

- 🐍 Python 3.11
- ⚡ FastAPI (Backend API)
- 🌐 Streamlit (Frontend UI)
- 🔐 passlib (Password Hashing)
- 🧠 LangChain + ChromaDB (Vector Store)
- 🗃️ SQLite (Local database)

## 🖥️ Architecture Diagram
![Architecture Diagram](Codebasics_RBAC_RAG_Chatbot/images
/Architecture.jpg)


## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/BhavyaJethwa/Codebasics_RBAC_RAG_Chatbot.git
cd Codebasics_RBAC_RAG_Chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run FastAPI Backend

```bash
uvicorn main:app --reload
```

### 5. Run Streamlit Frontend

```bash
streamlit run app.py
```

## 🔐 Default Admin Credentials

```text
Username: Admin
Password: adminpass
```

> ⚠️ Change the default credentials after first login.

## 🗂️ Folder Structure

```
.
├── backend/
│   ├── main.py               # FastAPI backend
│   ├── app.log               # Logging
│   ├── __init__.py
│   ├── chroma_db/            # Vector store (FAISS)
│   ├── RAG/                  # RAG logic
│   ├── resources/            # Uploaded documents
│   ├── schemas/              # Pydantic models
│   ├── services/             # Auth, user, and chatbot services
│   └── utils/                # Utility and database logic
│
├── streamlit/
│   └── frontend.py           # Streamlit frontend
│
├── .env                      # Environment variables
├── .gitignore
├── FinSolve.db               # SQLite database
├── requirements.txt
└── README.md
```

## 📚 Roles Supported

- admin
- hr
- finance
- marketing
- engineering
- general or employee
- executive

You can create and assign more roles dynamically via the Admin panel.

## ✅ Admin Capabilities

- Add new users
- Create new roles
- Upload documents for specific roles
- Reset password for users

## 📦 API Endpoints (FastAPI)

- `POST /login` - Authenticate user
- `POST /register` - Register a new user
- `POST /add_role` - Add a new role (Admin only)
- `POST /add_docs_role` - Upload document per role
- `POST /chat` - Ask a question (RAG-based)
- `POST /reset_password` - Reset user password
- `GET /get_roles` - Get list of roles

## ✅ To-Do / Future Enhancements

- [ ] JWT-based authentication
- [ ] Email verification for password resets
- [ ] Deployment using Docker & Nginx
- [ ] Analytics Dashboard for Admins

## 🤝 Contributing

Feel free to fork the project and raise a pull request if you have suggestions or improvements!

