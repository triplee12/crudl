# pull official base image
FROM python:3.10.1

# accept arguments
ARG PIP_REQUIREMENTS=production.txt

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip setuptools

# create user for the Django project
RUN useradd -ms /bin/bash crudl

# set current user
USER crudl

# set work directory
WORKDIR /home/crudl

# create and activate virtual environment
RUN python3 -m venv crudl_env

# copy and install pip requirments
COPY --chown=crudl ./src/crudl/requirements /home/crudl/requirements/
RUN ./portfo/bin/pip3 install -r /home/crudl/requirements/${PIP_REQUIREMENTS}

# copy Django project files
COPY --chown=crudl ./src/crudl /home/crudl/