# Restaurant Menu

A simple command-line restaurant menu application built with **Python**, **PostgreSQL**, **Psycopg**, and **Docker Compose**.

The project is intended as a practical exercise for working with Python, SQL, PostgreSQL, Docker, input validation, and basic error handling.

## Features

Currently implemented:

- View the complete restaurant menu.
- Filter available products by category.
- Add new products to the database.
- Validate menu options and product data.
- Handle invalid numeric input without crashing the application.
- Handle PostgreSQL connection and query errors.
- Roll back failed database writes.
- Close the database connection safely when the application finishes.

Planned features:

- Search for a product.
- Modify a product.
- Delete a product.
- Change product availability.
- View unavailable products.
- View menu statistics.

## Product categories

The application currently supports four categories:

- `ENTRADA`
- `PRINCIPAL`
- `POSTRE`
- `BEBIDA`

## Technologies

- Python 3
- PostgreSQL 18
- Psycopg 3
- Docker
- Docker Compose

## Project structure

```text
restaurant-menu/
├── app.py
├── docker-compose.yaml
├── requirements.txt
├── .gitignore
└── README.md
```

## Database configuration

The Docker Compose configuration creates a PostgreSQL database with the following development settings:

```text
Database: carta_digital
User: anderson
Port: 5432
```

For a real deployment, credentials should not be stored directly in the source code. Environment variables or a `.env` file should be used instead.

## Database table

The application expects a `productos` table with the following structure:

```sql
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    valor NUMERIC(10, 2) NOT NULL,
    disponible BOOLEAN DEFAULT TRUE
);
```

Example data:

```sql
INSERT INTO productos (tipo, nombre, valor)
VALUES
('ENTRADA', 'EMPANADAS', 5000),
('PRINCIPAL', 'MILANESA CON PAPAS', 15000),
('POSTRE', 'FLAN', 6000),
('BEBIDA', 'COCA COLA', 3500);
```

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd restaurant-menu
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install "psycopg[binary]"
```

You can save the dependency list with:

```bash
pip freeze > requirements.txt
```

Later, dependencies can be installed with:

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL

```bash
docker compose up -d
```

Check that the container is running:

```bash
docker compose ps
```

### 5. Create the table

Open PostgreSQL:

```bash
docker compose exec db psql -U anderson -d carta_digital
```

Then execute the `CREATE TABLE` statement shown above.

Exit PostgreSQL with:

```text
\q
```

### 6. Run the application

```bash
python app.py
```

## Error handling

The application includes basic protections against common errors:

- Invalid menu options are requested again.
- Empty product names are rejected.
- Invalid prices such as letters or negative values are rejected.
- PostgreSQL connection errors are caught and displayed without a Python traceback.
- Failed `INSERT` operations execute `rollback()` so the connection remains usable.
- Database cursors and connections are closed using a `finally` block.
- `Ctrl+C` exits the application gracefully.

## Recommended `.gitignore`

```gitignore
.venv/
__pycache__/
*.pyc
.env
```

## Future improvements

The next steps for the project are to complete the remaining CRUD operations and move database credentials to environment variables.
