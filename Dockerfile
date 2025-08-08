# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . /app/

# Expose port 8000 to the outside world
EXPOSE 8000

# Define the command to run the application
# We run migrations first, then start the development server.
# Note: This is a simple way for a dev environment. For production, a more robust
# entrypoint script that waits for the database would be better.
CMD ["sh", "-c", "python exam_registration/manage.py migrate && python exam_registration/manage.py runserver 0.0.0.0:8000"]
