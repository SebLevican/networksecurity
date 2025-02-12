# Network Security for Phishing Data

A comprehensive solution developed in Python for analyzing and detecting phishing data, focused on network security. This project covers everything from data processing and validation to implementing predictive models, automated network traffic analysis, and cloud deployment using Docker and CI/CD.

## Table of Contents

- [Description](#description)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
  - [Running Locally](#running-locally)
  - [Running with Docker](#running-with-docker)
- [CI/CD](#cicd)
- [Deployment on GCP](#deployment-on-gcp)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Description

This project focuses on network security, providing a tool to detect and analyze phishing data. The solution automates data processing and validation, employs predictive models to identify suspicious patterns, and facilitates the implementation of a robust and scalable environment.

## Features

- **Data Processing and Validation:** Automates the cleaning and validation of network data.
- **Predictive Models:** Implements algorithms to identify patterns indicative of phishing activity.
- **Automated Traffic Analysis:** Continuously monitors and analyzes network traffic.
- **Docker Integration:** Simplifies deployment and ensures consistency across environments.
- **CI/CD with GitHub Actions:** Automates testing, Docker image building, and deployment.
- **Deployment on GCP:** The FastAPI application is deployed on a Google Cloud Compute Engine instance, running inside a Docker container.

## Technologies

- **Python:** Primary programming language.
- **FastAPI:** Framework for building fast and efficient APIs.
- **Docker:** Containerizes the application.
- **GitHub Actions:** Automates integration and continuous deployment.
- **Google Cloud Platform (GCP):** Deploys and hosts the application on Compute Engine.

## Installation

### Prerequisites

- Python 3.8 or higher
- Docker
- Git

### Creating a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### Installing Dependencies
pip install -r requirements.txt

### Usage
Running Locally

To run the application in development mode:
uvicorn app:app --reload

Then, access the interactive documentation at: http://127.0.0.1:8000/docs
Running with Docker

Build the Docker image:
docker build -t networksecurity .

Run the container:
docker run -d -p 8080:8080 networksecurity


CI/CD

This project uses GitHub Actions to automate testing, Docker image building, and deployment. The workflow configuration can be found in the .github/workflows directory.
Deployment on GCP

The FastAPI application is deployed on a Google Cloud Compute Engine instance, running inside a Docker container.
You can view the application in action at: http://34.58.103.177:8080/docs
Contributing

Contributions are welcome! If you want to improve the project or report an issue, please open an issue or submit a pull request.
License

This project is licensed under the MIT License. See the LICENSE file for more details.
Contact

For inquiries or suggestions, feel free to contact me via email.

### Cloning the Repository

```bash
git clone https://github.com/SebLevican/networksecurity.git
cd networksecurity ```
