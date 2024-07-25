# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.11.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install locales
RUN echo "uz_UZ.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen uz_UZ.UTF-8
ENV LANG uz_UZ.UTF-8
ENV LANGUAGE uz_UZ:uz
ENV LC_ALL uz_UZ.UTF-8

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /code/
COPY . /code/