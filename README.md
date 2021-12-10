The Eye
=======

User behavior analyzation tool


Overview
---------

Exposes a single syncronous endpoint that validates and logs recieved events.
Meant to be used with a log aggregation tool.


Local installation
------------------

Install requirements with

    pip3 install --upgrade -r requirements.pip

Edit .env file in the root directory of the project and add the following configuration entries:
- SECRET_KEY
- THE_EYE_LOGGING_LEVEL
- THE_EYE_DB_LOGGING_LEVEL
- THE_EYE_REQUEST_LOGGING_LEVEL
- THE_EYE_LOG_FILENAME
- EVENT_TRACKER_SHARED_SECRET

Create the default rotating log file or the file specified in THE_EYE_LOG_FILENAME
    touch local.log


Deploying
---------

Designed to work with Splunk. File monitor(https://docs.splunk.com/Documentation/Splunk/latest/Data/MonitorFilesandDirectories)
for the rotating log should be impleneted before app can be useful.


TODO
----

Implement a websocket endpoint for events
