# start by pulling the python image
FROM python:3.10-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# Install psql for psycopg2
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

EXPOSE 8080

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py"]