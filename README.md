The Eye
=======

User behavior analyzation tool


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

Create the default rotating log file
    touch local.log
