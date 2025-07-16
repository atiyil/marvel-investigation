# Marvel Investigation
## Overview
A python flask web application to provide data for investigation using Marvel API at https://developer.marvel.com/. The application works for any Marvel character including `Spectrum`.

## Prerequisites
- docker v20.10.5 or later
- docker-compose v1.28.5 or later

## Running
- Unzip the package and run `docker-compose up -d` in the folder of `docker-compose.yaml`
- Verify that containers are created and running by `docker ps`
- Open a browser and type in `http://127.0.0.1/`, then hit enter
- Wait 1-2 minutes for the application to complete API calls and save data to the database

## Testing
`pytest` has been used for automated testing and several examples are provided. Feel free to add more cases

## Assumptions
- Marvel API returns 100 results at most for main resource. Therefore, it is assumed that any character will have less than 100 comics. However, future development may allow multiple calls for the same step to handle pagination properly.
- Marvel API returns 20 results for other resources in the request, such as number of comics in a character request. Therefore, a specific call for comics must be performed to receive all comics for that character assuming it may be less than 100 but more than 20
- On the other hand, number of characters in a comic is usually less than 10. Therefore, it is assumed that a comic will have less than 20 characters
- Only 1 main character is expected. This can be easily updated to multiple main characters by allowing comma separated input and updating `util.helper.gather_data()` to handle it.

## Limitations
- The application supports up to 100 comics for a main character
- The characters in a comic can be at most 20
- The application allows only 1 main character

## Design Decisions
- a simple multi-container application seems the best option to prevent environment and database connection issues
- python framework `flask` is used to create a simple web application
- `mongodb` is used as it is a simple database and accepts JSON data which is like python dictionary
- `nginx` is used to handle web requests properly and makes application extensible and scalable along with containerization
- `json.loads` is used to parse GET response

## Future Development
- Improve handling of secrets, such as API Private Key, in a better way than using environment variable due to the issues mentioned at https://diogomonica.com/2017/03/27/why-you-shouldnt-use-env-variables-for-secret-data/. `secret` feature in `docker swarm` or using a vault may help
- Although mongodb container is only accesible by host, it will be better to change default port, create a db user with limited access and provide authentication for better security
- Allow multiple calls for the same step to handle pagination properly and solve the limitation of max 100 results
- The application can be converted to a pip package for easy installation and support. `setup.py` must be defined
- While extending this project, library and utility functions can be defined in `util` folder and automated tests can be added to `tests` folder
- More automated tests and inline comments must be added
- More error and exception handling should be added, main program has `try/except` block and this can be improved by handling different exception types
- More refactoring will be done
- It will be great if Marvel provides a graphQL interface for the current API.That may decrease number of client requests to get id fields for each resource. It will also provide faster response to the query
