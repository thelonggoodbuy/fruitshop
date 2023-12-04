# pull official base python image
FROM python:3.10.13
# FROM ubuntu:latest

# set the work directory inside docker image
WORKDIR /usr/src/app

# sen enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHOBUNBUFFERED 1

# install libraries
RUN apt update
# RUN apt install --virtual build-deps gcc python3-dev musl-dev
# RUN apt install postgresql-dev
RUN echo y|apt install postgresql  
RUN apt install postgresql-contrib
RUN apt install libpq-dev
RUN pip install psycopg2
# RUN apt remove build-deps
# RUN apt install --no-cache make
# (!!!)
RUN echo y|apt install wkhtmltopdf
RUN apt install -y netcat-traditional
RUN echo y|apt install supervisor
RUN apt install make



# install dependencies (!)
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

# copy entrypoint.dev.sh (!)
COPY ./entrypoint.dev.sh /usr/src/app/entrypoint.dev.sh
RUN chmod +x /usr/src/app/entrypoint.dev.sh

# copy project
COPY . /usr/src/app/
# RUN chmod 755 entrypoint.dev.sh

COPY supervisor/conf.d /etc/supervisor/conf.d/
RUN mkdir /run/daphne/
# RUN chown app:app /run/daphne/
RUN mkdir /usr/lib/tmpfiles.d/daphne.conf

EXPOSE 3000

# run entrypoint.sh
ENTRYPOINT [ "/usr/src/app/entrypoint.dev.sh" ]
# CMD ["run"]