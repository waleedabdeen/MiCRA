[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# Multi-label Classification of Requirements Artifacts (MiCRA)

A tool to demonstrate the multi-label classification of requirements artifacts, and its application.


## How to Develop

The project consist of two main parts, a backend and a frontend. In order to start development you need to bring up the backend and the frontend.

### Backend

Ensure that you have python `v 3.9` installed on your machine. 

1. Navigate to the `./backend/` folder using the terminal.
2. Create an copy of the environment file by running `cp .env.example .env`.
3. Install backend dependencies by running the command `pip install -r requirements.txt`. You should run this command evertime you pull the code from the repository and whenever you change the requirements file.
4. Start the server `python server.py`.


### Frontend

Ensure that you have at least npm `v 10.3.0`.

1. Navigate to the `./frontend/` folder using the terminal.
2. Create an copy of the environment file by running `cp .env.example .env`.
3. Install frontend dependencies by running the command `npm install`.
4. Start the frontend development server by running `npm start`.


## Docker

The Docker images provided with this repository are not tested, but rather a WIP. Please refer to [how to develop](#how-to-develop) until the docker images are finalized.

The `docker-compose.yaml` contains the build argument `REACT_APP_SERVER_URL` to tell the compiled frontend where the backend's API can be reached.
You have to set this arugment before you build and run the Docker container.

Use `docker compose up` to build and run the containerized version of the backend and frontend.


## Contribution Guidelines

Please follow these guidelines when submitting a pull request.

1. A pull request should have a title that describes its purpose. If there is a feature or a bug Id, then please add it here.
2. Summarize the list of made changes (preferabley using a list)
3. Test your code and provide any test cases that you used to verify the code.
4. Add a screenshot showing the test results.
5. Be patient

## License

Copyright © 2024 Waleed Abdeen

This work (source code) is licensed under [GPLv3](./LICENSE).
