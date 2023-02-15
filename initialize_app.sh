# Forces users to use this file correctly by sourcing it instead of running it via a new bash session
(
  [[ -n $ZSH_VERSION && $ZSH_EVAL_CONTEXT =~ :file$ ]] || 
  [[ -n $KSH_VERSION && "$(cd -- "$(dirname -- "$0")" && pwd -P)/$(basename -- "$0")" != "$(cd -- "$(dirname -- "${.sh.file}")" && pwd -P)/$(basename -- "${.sh.file}")" ]] || 
  [[ -n $BASH_VERSION ]] && (return 0 2>/dev/null)
) && sourced=1 || sourced=0
if [ "$sourced" -eq "0" ]; then
    echo "Usage: source ./initialize_app.sh"
    exit -1
fi


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

echo "Installing Python dependencies..."
source bot-env/bin/activate
python3 -m pip install -r requirements.txt
echo "Python virtual environment activated and initialized!"
echo "To deactivate, enter: deactivate"

if [ -f "./.process.env" ]; then
    echo "Using existing Python environment file: .process.env"
else
    echo "Creating environment file: .process.env"
cat << EOF > .process.env
DISCORD_AUTH_TOKEN="$discord_auth_token"
DATABASE_NAME="$database_name"
EOF
fi
