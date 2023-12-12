#!/bin/bash

for i in {1..99}
do
  EMAIL="user${i}@example.com"
  PASSWORD="password${i}"
  FIRST_NAME="FirstName${i}"
  LAST_NAME="LastName${i}"

  curl -X POST http://localhost:8000/users/register/ \
    -H 'Content-Type: application/json' \
    -d '{
      "email": "'"${EMAIL}"'",
      "password": "'"${PASSWORD}"'",
      "first_name": "'"${FIRST_NAME}"'",
      "last_name": "'"${LAST_NAME}"'"
    }'
done

EMAIL="test@gmail.com"
PASSWORD="1"
FIRST_NAME="Test"
LAST_NAME="User"

curl -X POST http://localhost:8000/users/register/ \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "'"${EMAIL}"'",
    "password": "'"${PASSWORD}"'",
    "first_name": "'"${FIRST_NAME}"'",
    "last_name": "'"${LAST_NAME}"'"
  }'
