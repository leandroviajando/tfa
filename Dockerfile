FROM --platform=linux/amd64 python:3.10

WORKDIR /tfa

COPY ./app/requirements.txt /tfa/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tfa/requirements.txt

COPY ./ /tfa/
ENV PYTHONPATH=/tfa

CMD "/tfa/start.sh"