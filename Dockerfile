FROM ubuntu

RUN apt-get update
RUN apt-get -y install python
RUN apt-get -y install python-pip

ADD ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

ADD ./start.py ./start.py
CMD ["python", "-u", "./start.py"]
