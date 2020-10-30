FROM python:3.8
WORKDIR /usr/src/app
COPY . .
RUN python setup.py install
RUN mkdir -p /usr/src/app/mnt
ENTRYPOINT ["ft"]
