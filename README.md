# A brevet time calculator with user authentication for CIS 322 #

Eliot Martin | eliotm@uoregon.edu

## Overview

This is a reimplementation of the RUSA ACP controle time calculator (https://rusa.org/octime_acp.html). There are three main parts to this calculator: The main API that allows the users to enter specific times and distances onto an HTML page that updates with calculated open/close times (according to algorithm described in "Algorithm for brevet calculations" section) using jQuery. Upon hitting the submit button on the page, the calculated open and close times are inserted into a MongoDB database. Finally, by hitting the display button, open and close values are printed on an separate HTML page. Next, there is a RESTful API that returns the calculated open and close times in csv or json format (assuming there is a logged in user) from the database. This is done by using the following requests:

- "http://host:port/listAll/csv" should return all open and close times in CSV format

- "http://host:port/listOpenOnly/csv" should return open times only in CSV format

- "http://host:port/listCloseOnly/csv" should return close times only in CSV format

- "http://host:port/listAll/json" should return all open and close times in JSON format

- "http://host:port/listOpenOnly/json" should return open times only in JSON format

- "http://host:port/listCloseOnly/json" should return close times only in JSON format

There is also an additional optional argument "top" that will display only the top k arguments. Usage is as follows:

- "http://host:port/listOpenOnly/csv?top=3" should return top 3 open times only (in ascending order) in CSV format
- "http://host:port/listOpenOnly/json?top=5" should return top 5 open times only (in ascending order) in JSON format
- "http://host:port/listCloseOnly/csv?top=6" should return top 5 close times only (in ascending order) in CSV format
- "http://host:port/listCloseOnly/json?top=4" should return top 4 close times only (in ascending order) in JSON format

Finally, the consumer program with a logged in interface and a logged out interface. To log in, one needs to register. Registering adds the user to the database. Once registered, the user can log in and access new information. Token-based authentication is used to protect user information in the database (described in more detail in "User Authentication" section). The Logged in interface will give the user the option to visit a secret page where they can access the contents of the database via the REST API.


## Algorithm for Brevet Calculations

Controle open and close times are calculated by dividing the controle distance by the maximum and minimum speeds, respectively (maximum and minimum speeds are outlined here https://rusa.org/pages/acp-brevet-control-times-calculator). This time is rounded to the nearest minute.

Furthermore, there is a small bias for closing times with controles under 60 km that is calculated by subtracting the controle distance from 60 and dividing by 60. This value is then added to the usual closing time.

Finally, each brevet distance has predetermined closing times. Thus, controles greater than the brevet distance get no additional time as the closing time is now based on the brevet.

## User Authentication

Upon registering, a hashed password, username, and id will be stored in the data base. Upon logging in, a request will be sent to the REST API for a token. Should the username exist and the hashed password from logging in match the hashed password in the data base, the server will respond with a token valid for ten minutes. This token will be used to validate subsequent requests made by the user. 

## USAGE
Build image and run in docker from brevets folder (where the dockerfile and yml file are located). 


## Credits

Michal Young, Ram Durairajan, Steven Walton, Joe Istas.
