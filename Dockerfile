# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables to avoid bytecode generation and buffer output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

## Install Redis
#RUN apt-get update && apt-get install -y redis-server

# Install Poetry
RUN pip install --upgrade pip \
    && pip install poetry

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh


# Run the entrypoint script
CMD ["/app/entrypoint.sh"]
