Project Requirements
--------------------
Depending on how you run it, you will need the following:

*1. Running the project using docker-compose*
Requirements:
- Docker engine (Yeah, that's it)

*2. Running the project without docker-compose*

Requirements:
 * Python 3.6 or higher

 * Poetry environment

 * Postgres: 12.0 or higher


Project Setup
=================

Information on how to setup the project.

Common steps:

#.  Create a folder name 'local' in the root of the project.

#. Create a file name 'settings.dev.py' in the 'local' folder.

#. You can copy the content of 'core/main/templates/settings.dev.py' to 'settings.dev.py'. Or you can create your own settings if needed. (optional)


Running the project using docker-compose:
-----------------------------------------
 #. Run the command: ``docker compose -f docker-compose.yml up``

Running the project without docker-compose:
-------------------------------------------

  #. Create a virtual environment using poetry
  #. Activate the virtual environment
  #. Install the dependencies using poetry: ``poetry install``
  #. Create a database in postgres
  #. Update database settings in ``core/main/settings/base.py``
  #. Run the migrations: ``poetry run python manage.py migrate``


Running tests
=============

*NOTE:* To run tests you will need to setup the environment as described above. (steps without docker)


To run the tests, you can use the following command:

``poetry run python -m core.manage test --keepdb``