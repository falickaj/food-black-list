FROM python:3.10


# Install pip requirements
WORKDIR /
COPY . /
RUN apt-get update
RUN python -m pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

CMD ["python3","app/app.py"]

