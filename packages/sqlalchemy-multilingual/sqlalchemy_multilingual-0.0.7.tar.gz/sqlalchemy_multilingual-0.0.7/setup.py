from setuptools import setup, find_packages

setup(
    packages=find_packages(
        where=[
            "src/sqlalchemy_multilingual",
            "src/sqlalchemy_multilingual/alembic"
        ],
        exclude=[".venv"]
    ),
)
