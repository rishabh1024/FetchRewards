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
