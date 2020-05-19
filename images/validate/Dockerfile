FROM python:3.7-slim-buster

# This dockerfile is kind of like a venv, but it also provides the input/output data (abstracting that from the script)

RUN pip install -U pandas && \
    pip install -U pandas-schema

COPY validate.py /validate.py

ENTRYPOINT ["python", "validate.py"]