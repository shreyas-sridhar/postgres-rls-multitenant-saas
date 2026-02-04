# Secure Multi-Tenant SaaS Backend with PostgreSQL RLS

**Technologies:** Python, Flask, PostgreSQL, SQLAlchemy, Row Level Security (RLS), REST APIs

*   Designed and implemented a high-security multi-tenant backend architecture ensuring strict data isolation for SaaS applications using **PostgreSQL Row Level Security (RLS)**.
*   Engineered a **Flask** middleware system to automatically inject tenant context (`SET LOCAL app.current_tenant`) into database sessions, eliminating the risk of data leaks caused by application-layer logic errors.
*   Built a clean, scalable **REST API** using the **Application Factory** pattern, separating concerns into Routes, Services, and Models.
*   Optimized database schema with **UUIDs** and specific RLS policies (`USING` & `WITH CHECK`) to enforce read/write access controls at the database kernel level.
*   Developed automated verification scripts to validate tenant isolation boundaries, ensuring 100% data integrity between concurrent tenants.
