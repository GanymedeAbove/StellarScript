#!/bin/bash

# Define the project directory
project_dir="Mybirthchart"

# Function to check and install Python, pip, and virtualenv
install_python_deps() {
    echo "Checking for Python, pip, and virtualenv..."
    
    # Install Python3 if not present
    if ! command -v python3 &>/dev/null; then
        echo "Python3 is not installed. Installing Python3..."
        sudo apt-get update && sudo apt-get install python3
    else
        echo "Python3 is already installed."
    fi

    # Install pip if not present
    if ! command -v pip3 &>/dev/null; then
        echo "pip is not installed. Installing pip..."
        sudo apt-get install python3-pip
    fi

    # Install virtualenv if not present
    if ! pip3 show virtualenv &>/dev/null; then
        echo "virtualenv is not installed. Installing virtualenv..."
        pip3 install virtualenv
    fi
}

# Function to set up the project environment and dependencies
setup_environment() {
    echo "Setting up the project environment..."

    # Create project directory
    mkdir -p $project_dir
    cd $project_dir

    # Create and activate virtual environment
    virtualenv venv
    source venv/bin/activate

    # Install pyswisseph
    pip install pyswisseph

    echo "Environment setup complete. All dependencies are installed."
}

# Main script execution starts here
echo "Starting the setup script for the astrological project..."

# Install Python and its tools if necessary
install_python_deps

# Prompt user to continue with the setup
read -p "Proceed with setting up the environment? (y/n): " proceed
if [[ $proceed == [Yy] ]]; then
    setup_environment
    echo "Setup completed successfully. You can now run the astrological calculations."
else
    echo "Setup canceled by user."
    exit 1
fi
