# FetchRewards

Receipt Processor Challenge for Fetch Rewards

## Overview

This project is a receipt processor API built with FastAPI. It allows users to submit receipts for processing and retrieve the points awarded for each receipt.

## API Endpoints

### 1. Process Receipts

- **Endpoint**: `/receipts/process`
- **Method**: `POST`
- **Description**: Submits a receipt for processing.
- **Request Body**: JSON object representing the receipt.
- **Response**: JSON object containing a unique ID for the receipt.

**Example Response**:
```json
{
  "id": "7fb1377b-b223-49d9-a31a-5a02701dd310"
}
```

### 2. Get Points

- **Endpoint**: `/receipts/{id}/points`
- **Method**: `GET`
- **Description**: Retrieves the points awarded for the receipt with the given ID.
- **Response**: JSON object containing the number of points awarded.

**Example Response**:
```json
{
  "points": 32
}
```

## Running the API with Docker

To run the API using Docker, follow these steps:

1. Navigate to the project directory:
   ```sh
   cd FetchRewards
   ```

2. Build the Docker image:
   ```sh
   docker build -t receipt-processor-api .
   ```

3. Run the Docker container:
   ```sh
   docker run -p 5000:8000 receipt-processor-api
   ```

The API will be accessible at `http://127.0.0.1:5000`.

## Using the API

### Process a Receipt

To process a receipt, send a `POST` request to `http://127.0.0.1:5000/receipts/process` with the receipt data in the request body. This will return a unique ID for the receipt.

### Get Points for a Receipt

To get the points for a receipt, send a `GET` request to `http://127.0.0.1:5000/receipts/{id}/points` with the receipt ID in the URL. This will return the number of points awarded for the receipt.

## Swagger UI

You can also interact with the API using the Swagger UI at `http://127.0.0.1:5000/docs`.
