FROM python:3.12-slim

COPY requirements.txt /tmp

RUN pip install --no-cache -r /tmp/requirements.txt

COPY InventoryETL.ipynb /usr/src

ENTRYPOINT ["bash", "-c", "papermill /usr/src/InventoryETL.ipynb /tmp/output.ipynb && jupyter nbconvert --to html --output-dir /outputs /tmp/output.ipynb"]
