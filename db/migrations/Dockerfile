FROM python:3.10-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the necessary files to the container (assuming alembic-related files are in the current directory)
COPY . .

# Install psql for psycopg2
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Install any required dependencies for Alembic migrations
RUN pip install alembic sqlalchemy psycopg2-binary python-dotenv

# Set the entrypoint command to execute Alembic migrations
CMD ["alembic", "upgrade", "head"]
