# pull official base python image
FROM python:3.10.13-alpine

# set the work directory inside docker image
WORKDIR /usr/src/app

# sen enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHOBUNBUFFERED 1

# install libraries
RUN apk update
RUN apk add --virtual build-deps gcc python3-dev musl-dev
RUN apk add postgresql-dev
RUN pip install psycopg2
RUN apk del build-deps
RUN apk add --no-cache make

# install dependencies (!)
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt

# copy entrypoint.dev.sh (!)
COPY ./entrypoint.dev.sh /usr/src/app/entrypoint.dev.sh
RUN chmod +x /usr/src/app/entrypoint.dev.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT [ "/usr/src/app/entrypoint.dev.sh" ]