FROM ubuntu:14.04
MAINTAINER Robert Thompson <rthompsonj@gmail.com>

# system packages
RUN apt-get update && apt-get install -y curl

# get miniconda
RUN curl -OL http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
RUN bash Miniconda-latest-Linux-x86_64.sh -p /miniconda -b
RUN rm Miniconda-latest-Linux-x86_64.sh
ENV PATH=/miniconda/bin:${PATH}
RUN conda update -y conda

# python packages via conda
RUN conda install -y \
    flask \
    numpy \
    scipy \
    scikit-learn \
    pandas

COPY app /app
COPY model /model
WORKDIR "/app"

expose 5000

ENTRYPOINT ["/miniconda/bin/python", "flask_app.py"]