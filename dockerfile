# Use an official Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /receipt-processor-challenge

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port that Uvicorn will run on
EXPOSE 8000

# Command to run Uvicorn with FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]