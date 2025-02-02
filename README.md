# Receipt Processor Web Service
This is a FastAPI-based web service that proccesses receipts and awards points.

## Setup Instructions

### Clone the repository
```
git clone https://github.com/caelaintrtas/receipt-processor.git
cd receipt-processor
```

###Run with Docker
```
docker build -t receipt-processor .
docker run -p 8000:8000 receipt-processor
```
The API will be accessible at http://127.0.0.1:8000/ for making requests.

##Running Tests
To run tests inside the Docker container:
```
docker exec -it <container_id> pytest
```
To run tests locally:
```
pytest
```
