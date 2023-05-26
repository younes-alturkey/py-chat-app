FROM python:3
RUN pip3 install colorama
ADD loadbalancer.py config.py /
CMD [ "python", "./loadbalancer.py" ]