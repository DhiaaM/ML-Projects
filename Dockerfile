
FROM ubuntu:18.04

LABEL maintainer="Amazon AI <sage-learner@amazon.com>"


RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3-pip \
         python3-setuptools \
         nginx \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

RUN pip --no-cache-dir install numpy scikit-learn==0.20.2 pandas 
# flask gunicorn


ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="C:\Users\Dhiaa Mejdi\Documents\ML-Projects:${PATH}"


COPY app-ML.py /app.py
COPY model.pickle /model.pickle