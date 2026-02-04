# Flask Multi-Tenant SaaS Backend with PostgreSQL RLS

A production-grade, backend-only Multi-Tenant SaaS application demonstrating **hard** tenant isolation at the database layer using **PostgreSQL Row Level Security (RLS)**.

## 🚀 Key Features

*   **Database-Level Isolation**: Tenant data is isolated using PostgreSQL RLS policies, not just application logic.
*   **Flask Application Factory**: Scalable and testable application structure.
*   **SQLAlchemy ORM**: Clean data access layer with session handling.
*   **RLS Injection Middleware**: Automatically injects `X-Tenant-ID` into the database session context.
*   **REST API**: Endpoints for managing tenants and projects.

## 🛠️ Tech Stack

*   **Language**: Python 3.x
*   **Framework**: Flask
*   **Database**: PostgreSQL
*   **ORM**: SQLAlchemy
*   **Security**: Row Level Security (RLS)

## 📂 Project Structure

```
flask_rls_saas/
├── app/
│   ├── models/          # Database Models
│   ├── routes/          # API Routes (Blueprints)
│   ├── services/        # Business Logic
│   ├── __init__.py      # App Factory
│   ├── config.py        # Settings
│   ├── db.py            # DB Setup & RLS Helper
│   └── middleware.py    # Context Injection
├── scripts/
│   └── init_db.sql      # Schema & RLS Policies
├── requirements.txt
├── run.py               # Entry Point
└── test_rls.py          # Verification Script
```

## ⚡ Setup & Run

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Database**:
    *   Ensure PostgreSQL is running.
    *   Create a database named `flask_rls_saas`.
    *   Run the SQL script to create tables and policies:
        ```bash
        psql -U postgres -d flask_rls_saas -f scripts/init_db.sql
        ```
    *   *Note: Update `SQLALCHEMY_DATABASE_URI` in `app/config.py` if your credentials differ.*

3.  **Run the Server**:
    ```bash
    python run.py
    ```

4.  **Verify Isolation**:
    Run the included test script to verify that Tenant A cannot see Tenant B's data:
    ```bash
    python test_rls.py
    ```

## 🔒 Security Architecture

The application uses a **Shared Database, Shared Schema** approach but enforces isolation via **RLS**.

1.  **Request**: Client sends `X-Tenant-ID` header.
2.  **Middleware**: `app/middleware.py` intercepts the request, reads the header, and executes `SET LOCAL app.current_tenant = 'UUID'`.
3.  **Database**: PostgreSQL checks every query against RLS policies defined in `init_db.sql`.
    *   `creating projects`: Enforced by `WITH CHECK` clause.
    *   `listing projects`: Enforced by `USING` clause.

This ensures that even if a developer forgets to add `filter_by(tenant_id=...)` in the code, the database will return **zero rows** for other tenants.
