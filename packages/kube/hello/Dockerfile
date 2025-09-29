#--docker "nuvolaris/aigency-runtimes:python_v3.12-2506091954.1060304ecbd5"
FROM apache/openserverless-runtime-python:v3.12-2506091954
USER root
ADD pyproject.toml pyproject.toml
RUN pip3 install .
USER nobody
