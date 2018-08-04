FROM alpine

LABEL author="Chris Lee"
LABEL email="sihrc.c.lee@gmail.com"

COPY requirements.txt /requirements.txt
RUN apk update && \
    apk add --no-cache build-base \
    python3-dev \
    python3 \
    bash && \
    python3 -m ensurepip && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    pip3 install --upgrade pip wheel && \
    rm -r /root/.cache && \
    pip3 install -r requirements.txt

COPY . /vortex
WORKDIR vortex

RUN python3 setup.py develop

CMD ["bash"]