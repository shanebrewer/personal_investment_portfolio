# PYTHON ENVIRONMENT SETUP

`virtualenv ./.venv`
`pip install -r requirements.txt`


# DYNAMO DB SETUP

https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html

cd /mnt/d/program_files/DynamoDBLocal
Run the command:
`java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb`
