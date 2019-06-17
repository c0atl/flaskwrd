FROM ubuntu:latest
ENV PASSWD_FILE /var/passwd
ENV GROUP_FILE /var/group
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app/flaskwrd.py"]
