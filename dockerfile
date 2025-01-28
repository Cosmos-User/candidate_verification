# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Install libGL
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .



# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 7001

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7001"]