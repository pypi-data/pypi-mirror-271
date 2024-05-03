FROM jupyter/base-notebook:latest
#FROM jupyter/scipy-notebook:latest

# install gcc and dependencies useful to build some libraries/wheels
USER root
RUN apt update && apt install build-essential -y --no-install-recommends
RUN groupadd --gid 1050 microservices && usermod -aG microservices jovyan

USER ${NB_UID}
ARG PIP_INDEX_URL
RUN pip install pipx uv

# conda already runs in a venv so uv venv not required!
env CONDA_PREFIX=/opt/conda

COPY jupyterlab/requirements.txt .
RUN uv pip install -r ~/requirements.txt
