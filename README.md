# Python Coding Challenge
Hello, and welcome to the Python coding challenge!  You'll find a set of instructions below that you must attempt to complete within 3 days.  Clone this repository to start the challenge, and good luck!   When completed, push your solution to a new repository, and send us a link.

Within this repository, you will find a hastily thrown together application.  It's a very basic, a simple To-Do API with the ability to create and list your to-dos.

Here are some things we need help with:

- We have create and list features but lack the ability to update.  Introduce a new PUT endpoint at `/todos/{todoID}` that receives a JSON body containing title and status.  The feature should update the existing record and return a JSON body representing the updated todo item.

- You may notice the lack of tests.  Consider setting a good example by adding tests to your method if you have time, so that the other devs can copy/paste from your good example.  Don't forget to update this README with instructions for how to run the tests!

- As mentioned before, we have create and list already in place.  The dev team was super excited because they knocked this out faster than anyone thought - maybe too fast!  As such, you may find a number of issues with this repo.  Feel free to correct any issues you may find.

# Setup
Within the repo you will find a `docker-compose.yaml` file. If you're familiar with docker and docker-compose, great! You can get started by simply running `docker-compose up` and that will create an API and Postgres container for you.

If you are not familiar with those tools, feel free to setup whatever environment you are comfortable working within. At the very least you will need a Python environment to run your API and a Postgres database. There is a `todo_schema.sql` file that will create a basic table and sequence to get you started. To run the API, simply run `uwsgi uwsgi.ini --py-auto-reload 1 --worker-reload-mercy 5`. You will need a few variables within the app, so please make sure those are provided:

- DB_USER
- DB_PASSWORD
- DB_NAME

Also, regardless of which environment you use, you'll need to install dependencies. For this repo, we are using [pip](https://pypi.org/project/pip/).
