# Use Python 3.12 slim image to match pyproject.toml (>=3.12) and keep image size small
FROM python:3.12-slim

# Set container working directory
WORKDIR /code

# Copy and install Python dependencies first to leverage Docker layer caching
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application source code
COPY ./src /code/src

# Document the port FastAPI listens on
EXPOSE 80

# Start FastAPI in production mode on port 80
CMD ["fastapi", "run", "src/main.py", "--port", "80"]
