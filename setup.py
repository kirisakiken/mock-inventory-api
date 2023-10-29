from setuptools import setup, find_packages

setup(
    name="tx-inventory-api",
    version="0.1",
    author="Bezmican Zehir",
    packages=find_packages(),
    install_requires=[
        "fastapi ~= 0.100.0",
        "uvicorn ~= 0.23.1",
        "sqlalchemy ~= 2.0.19",
        "pydantic ~= 2.4.2",
        "psycopg2 ~= 2.9.9",
        "databases[postgresql] ~= 0.4.2",
        "alembic ~= 1.6.5",
    ],
    extras_require={
        "dev": [
            "flake8 ~= 6.1.0",
        ],
        "test": [
            "pytest ~= 6.2.4",
            "ddt ~= 1.4.2",
        ],
    },
)