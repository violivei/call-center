FROM python:3
ADD ./ call-center/
WORKDIR call-center
RUN pip install -r requirements.txt
CMD [ "python", "./main.py" ]