# Use an official Python 3.10 runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the requirements file into the container
COPY requirements_all.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements_all.txt


python3.10 -m venv .mechagentai


# Copy the rest of your application code (if any)
COPY . .

# Define the command to run your application (modify as needed)
# CMD ["python", "your_script_name.py"]
