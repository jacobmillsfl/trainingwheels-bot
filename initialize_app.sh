#!/bin/bash

echo "* * * * Training Wheels Bot Environment Initializer * * * *"
echo ""
echo "      This script creates the initial files needed to"
echo "      run this application, including a Python"
echo "      virtual environment."
echo ""
echo "      You do not need to run this script more than once"
echo "      unless Python dependencies change."
echo ""
echo "      When running locally, don't worry about a Discord"
echo "      Auth Token. The default database name is: db.json"
echo ""

# Allow user to specify custom environment variables

read -p "Enter Discord Auth Token (default: \"\"): " discord_auth_token
if [[ -z "$discord_auth_token" ]]; then
    discord_auth_token=""
    echo "Using empty string for Discord Auth Token"
fi

read -p "Enter Database Name (default: \"db.json\"): " database_name
if [[ -z "$database_name" ]]; then
    database_name="db.json"
    echo "Using \"db.json\" for Database Name"
else
    if [[ $database_name != *\.json ]]; then
        echo "Renaming database to: $database_name.json"
        database_name="$database_name.json"
    fi
fi

if [ -d "./bot-env" ]; then
    echo "Using existing Python environment: bot-env"
else
    echo "Creating new Python environment: bot-env"
    python3 -m venv bot-env
fi

if [ -f "./.process.env" ]; then
    echo "Using existing Python environment file: .process.env"
else
    echo "Creating environment file: .process.env"
cat << EOF > .process.env
DISCORD_AUTH_TOKEN=$discord_auth_token
DATABASE_NAME=$database_name
EOF
fi
