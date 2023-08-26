FROM --platform=linux/amd64 python:3.10

WORKDIR /tfa/app

COPY ./requirements.txt /tfa/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tfa/app/requirements.txt

COPY ./ /tfa/app/
ENV PYTHONPATH=/tfa/app

CMD "/tfa/app/start.sh"
# CMD ["sleep", "infinity"]
