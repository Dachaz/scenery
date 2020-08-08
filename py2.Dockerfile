FROM python:2

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /usr/src/scenery

COPY ./ /usr/src/scenery

ENTRYPOINT pyb
