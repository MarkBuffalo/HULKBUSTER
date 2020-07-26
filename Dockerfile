FROM python:3.7.4

ADD grab.py /
ADD requirements.txt /
ADD products.txt /
ADD wake_up.wav /
RUN pip3 install --upgrade pip playsound
RUN pip3 install -r requirements.txt
CMD [ "python3", "grab.py" ]
