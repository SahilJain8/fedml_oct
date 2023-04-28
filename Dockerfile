# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project to the container
COPY . .

# Expose the default Django port
EXPOSE 8000

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=myproject.settings
ENV PYTHONUNBUFFERED=1

# Run Django when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
