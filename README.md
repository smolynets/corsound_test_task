# Python Software Developer Home Assignment July 2024

#### OpenAPI/Swagger Specification:
Provide a detailed specification of the API in OpenAPI/Swagger format - /docs or /redoc

#### Python Web Framework:
Implement the solution using fastAPI microframework with https://huggingface.co/google/mobilenet_v2_1.0_224

#### Test Data:
Use /upload-image/ endpoint to updoud image (jpeg or png only)

#### Example of response: 
{
  "predictions": [
    {
      "class": "fox squirrel, eastern fox squirrel, Sciurus niger",
      "probability": 0.19683454930782318
    },
    {
      "class": "red fox, Vulpes vulpes",
      "probability": 0.19188515841960907
    },
    {
      "class": "dhole, Cuon alpinus",
      "probability": 0.0856076255440712
    }
  ]
}


#### Setup:

##### Run in project root directory:
	docker-compose up -d

##### Fow run all unit tests:
    docker exec -it backend pytest

##### Fow run particular unit tests:
    docker exec -it backend pytest -k test_name
