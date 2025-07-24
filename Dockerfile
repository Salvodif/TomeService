# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code to the working directory
COPY . .

# Set environment variables
# These can be overridden at runtime
ENV TOMESERVICE_LIBRARY_PATH=/data/library
ENV TOMESERVICE_DB_FILE=library.json

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "server.py"]
