FROM python:3.10-slim

RUN pip install --no-cach-dir pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock* /app/

RUN pipenv install --deploy --ignore-pipfile

COPY . .

EXPOSE 8000

RUN pipenv run pytest tests
CMD ["pipenv", "run", "python", "app.py"]