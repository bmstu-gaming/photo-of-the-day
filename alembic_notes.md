# Async Alembic

To use existing async engine init alembic like this:
```bash
alembic init -t async alembic
```

# Migration commands

Autogenerate revision:
```bash
alembic revision --autogenerate -m "Created users table"
```

Apply migration:
```bash
alembic upgrade head
```

> WARNINIG: Do not remove migration before downgrade, only after
```bash
alembic downgrade -1
```
Or:
```bash
alembic downgrade base
```
