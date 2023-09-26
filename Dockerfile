FROM python:3.11

WORKDIR /parrot

COPY ./requirements.txt /parrot/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /parrot/requirements.txt

COPY ./app /parrot/app

ENV PYTHONPATH=/parrot
ENV RULES_BASE_PATH=/parrot

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
