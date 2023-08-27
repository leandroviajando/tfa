FROM --platform=linux/amd64 python:3.10

WORKDIR /tfa/notebooks

COPY ./requirements.txt /tfa/notebooks/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tfa/notebooks/requirements.txt

COPY ./ /tfa/notebooks/
ENV PYTHONPATH=/tfa/notebooks

CMD ["jupyter", "notebook", "--no-browser", "--allow-root", "--ip=0.0.0.0", "--NotebookApp.token=''", "--NotebookApp.password=''"]
# CMD ["sleep", "infinity"]
