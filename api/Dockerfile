FROM python:3.12-slim

COPY requirements.txt /tmp

RUN pip install --no-cache -r /tmp/requirements.txt

COPY products_api /usr/src/products_api

WORKDIR /usr/src

ENTRYPOINT ["fastapi", "run", "products_api/main.py"]
