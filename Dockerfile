# Use an official Python runtime as a parent image
FROM python:3.5-slim

# Set the working directory to /worker
WORKDIR /worker

# Copy the current directory contents into the container at /app
ADD worker.py requirements.txt github-token ./

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "worker.py"]
