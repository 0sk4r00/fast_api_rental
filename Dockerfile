FROM python:3.10

WORKDIR /usr/src/app

COPY pyproject.toml ./

RUN pip install poetry

RUN poetry install --no-root --without dev

COPY . .

CMD ["uvicorn", "app.main:app", "--host","0.0.0.0", "--port", "8001"]