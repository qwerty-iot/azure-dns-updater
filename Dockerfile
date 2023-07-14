FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install azure-identity azure-mgmt-dns requests

# Copy python script
COPY ./script.py .

# Command to run the script
CMD ["python", "./script.py"]
