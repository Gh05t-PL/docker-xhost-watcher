# Use a lightweight Python base image
FROM python:3.9-slim

# Install Docker SDK for Python
RUN pip install docker schedule

# Copy the Python script into the container
COPY ./ /app/

# Command to run the monitoring script
CMD ["python3", "-u", "/app/main.py"]

# docker run --name monitor-all-containers --rm --privileged -v /var/run/docker.sock:/var/run/docker.sock hosts-monitor-all

