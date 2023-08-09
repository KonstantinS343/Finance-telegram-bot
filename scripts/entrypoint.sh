#!/bin/bash

cd alembic/

alembic upgrade head

cd ../src

python main.py