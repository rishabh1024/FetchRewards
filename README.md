# FetchRewards
Receipt Processor Challenge for Fetch Rewards


Summary of API Specification
Endpoint: Process Receipts

    Path: /receipts/process
    Method: POST
    Payload: Receipt JSON
    Response: JSON containing an id for the receipt.

Example Response:

{ "id": "7fb1377b-b223-49d9-a31a-5a02701dd310" }

Endpoint: Get Points

    Path: /receipts/{id}/points
    Method: GET
    Response: A JSON object containing the number of points awarded.

A simple Getter endpoint that looks up the receipt by the ID and returns an object specifying the points awarded.

Example Response:

{ "points": 32 }

In order to execute this api we need to have docker.
Commands to execute in order to run this api:

1. ``` cd FetchRewards ```
2. ```docker build -t receipt-processor-api .```
3. ```docker run -p 5000:8000 receipt-processor-api ```

The POST API for processing a receipt is http://127.0.0.1:5000/receipts/process. This will return a unique uuid as response.
The GET API for getting the points for a particular receipt with a give id(unique uuid) http://127.0.0.1:5000/receipts/{id}/points

THE API CAN ALSO BE EXECUTED USING SWAGGER UI: http://127.0.0.1:5000/docs#/
