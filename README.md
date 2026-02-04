# Flask Multi-Tenant SaaS Backend with PostgreSQL RLS

This repository contains a production-ready backend implementation for a Multi-Tenant SaaS application. It focuses on achieving hard tenant isolation at the database layer using PostgreSQL Row Level Security (RLS), ensuring that data partitioning is enforced by the database engine rather than relying solely on application-level filtering.

Tenant isolation is enforced at the database layer using PostgreSQL Row Level Security, making cross-tenant data access impossible even in the presence of application bugs

## Core Features

* **Database-Level Isolation**: Implements PostgreSQL RLS policies to prevent cross-tenant data leakage.
* **Flask Application Factory**: Utilizes a modular structure designed for scalability and simplified testing.
* **SQLAlchemy ORM**: Features a clean data access layer with managed session handling.
* **Context Injection Middleware**: Automatically extracts the `X-Tenant-ID` from incoming requests and injects it into the PostgreSQL session context.
* **REST API**: Includes pre-configured endpoints for tenant management and project resources.

## Technical Stack

* **Language**: Python 3.x
* **Framework**: Flask
* **Database**: PostgreSQL
* **ORM**: SQLAlchemy
* **Security**: Row Level Security (RLS)

## Project Structure

```
flask_rls_saas/
├── app/
│   ├── models/          # Database Models
│   ├── routes/          # API Routes (Blueprints)
│   ├── services/        # Business Logic
│   ├── __init__.py      # App Factory
│   ├── config.py        # Environment Settings
│   ├── db.py            # Database Setup and RLS Helpers
│   └── middleware.py    # Request Context Injection
├── scripts/
│   └── init_db.sql      # Schema definitions and RLS Policies
├── requirements.txt
├── run.py               # Application Entry Point
└── test_rls.py          # Isolation Verification Script

```

## Installation and Deployment

### 1. Install Dependencies

Execute the following command to install the required Python packages:

```bash
pip install -r requirements.txt

```

### 2. Database Configuration

* Ensure a PostgreSQL instance is active.
* Create a new database titled `flask_rls_saas`.
* Execute the SQL initialization script to set up the schema and RLS policies:
```bash
psql -U postgres -d flask_rls_saas -f scripts/init_db.sql

```


* Update the `SQLALCHEMY_DATABASE_URI` in `app/config.py` to match your local credentials.

### 3. Start the Application

Initialize the Flask development server:

```bash
python run.py

```

### 4. Verification

To ensure that RLS is functioning correctly and Tenant A cannot access Tenant B's records, run the verification suite:

```bash
python test_rls.py

```

---

## Security Architecture

The system operates on a **Shared Database, Shared Schema** model. Security is enforced through a multi-step handshake between the application and the database:

1. **Request Handling**: The client includes an `X-Tenant-ID` header in the HTTP request.
2. **Context Setting**: The middleware in `app/middleware.py` captures this ID and executes a `SET LOCAL app.current_tenant = 'tenant_uuid'` command within the current database transaction.
3. **Policy Enforcement**: PostgreSQL evaluates all queries against the policies defined in `init_db.sql`:
* **Data Insertion**: Validated via the `WITH CHECK` clause.
* **Data Retrieval**: Filtered via the `USING` clause.



By anchoring security in the database, the system provides a fail-safe mechanism. Even if a developer omits a tenant filter in a SQLAlchemy query, the database will inherently restrict the result set to the authorized tenant context.

## Future Additions:
1. Plan to add feature like git blame to store who accessed data outside their paygrade for a lack of a better term (Priority 1)
2. Will also add role separation (p3)
3. A frontend might help as well (P2)
