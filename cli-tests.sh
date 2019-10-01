#!/usr/bin/env bash
# prepare a db with a database named the same as your defaultdb + "_test"
# use pip install pytest==3.6.1 don't know the convention when we have a requirements.txt file
DB_NAME=$DB_NAME"_test"
pytest tests
