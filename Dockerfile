ARG PYTHON_VERSION=3.11


FROM python:$PYTHON_VERSION

WORKDIR /app

COPY pyproject.toml .
COPY README.md .
COPY requirements* .

RUN pip install -r requirements.txt
RUN pip install .


ENTRYPOINT ["python", "-m", "pytest"]


