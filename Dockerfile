FROM tiangolo/uvicorn-gunicorn:python3.7
WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system
COPY . /app