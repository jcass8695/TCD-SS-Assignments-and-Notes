# Use an official Python runtime as a parent image
FROM python:3.5-slim

# Set the working directory to /app
WORKDIR /worker

# Copy the current directory contents into the container at /app
ADD worker.py requirements.txt github-token ./

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

ENV http_proxy http://www-proxy.scss.tcd.ie:8080
ENV https_proxy http://www-proxy.scss.tcd.ie:8080

# Run app.py when the container launches
CMD ["python", "worker.py"]
