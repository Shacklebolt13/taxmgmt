# Tax Management System

## Build the docker image
`docker-compose -f /location/to/docker-compose.yml build`


## Run the docker container

    docker-compose -f /location/to/docker-compose.yml up
##  Access the Site

 - Open Any Browser
 - the site is hosted on 8000 port, using Django's Own Hosting Engine
	 - open  ` <container_ip>:8000`

## Api Docs
visit `http://<site_url>/docs/` to access the api documentation generated by DRF_YASG

## Authentication For Api

the api uses DRF's Token Auth. to authenticate, in **header** send the following pair :-
Authentication : "Token < token >"

Api Login can be done via `/api/auth/` end point. Send data as
username : < username >
password : < password >

## Rest of the UI can be accessed directly via the site itself
## Thanks a lot for this opportunity to prove my worth, looking forward for the results of my evaluation .
