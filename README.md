# clean_mss_template
Template for microservices repositories based in Clean Arch

## Installation
Clone the repository using template

### Create virtual ambient in python (only first time)
###### Windows
    python -m venv venv
###### Linux
    virtualenv -p python3.9 venv

### Activate the venv
###### Windows:
    venv\Scripts\activate
###### Linux:
    source venv/bin/activate

### Install the requirements
    pip install -r requirements-dev.txt

### Run the tests
    pytest

### To run local set .env file
    STAGE = TEST
