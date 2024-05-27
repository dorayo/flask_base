#!/bin/bash
rm -rf .git
rm -rf venv

# Ask for the project name
echo "Enter the project name:"
read project_name

# Rename flask_base.py to ${project_name}.py
mv flask_base.py "${project_name}.py"

# Check the operating system and execute the appropriate command
if [[ "$OSTYPE" == "darwin"* ]]; then
    # MacOS
    perl -i -pe "s/[Ff]lask_base/${project_name}/gi" README.md config.py
    find scripts -type f -not -name 'setup.sh' -exec perl -i -pe "s/[Ff]lask_base/${project_name}/gi" {} +
else
    # Linux and others
    sed -i "s/[Ff]lask_base/${project_name}/gI" README.md config.py
    find scripts -type f -not -name 'setup.sh' -exec sed -i "s/[Ff]lask_base/${project_name}/gI" {} +
fi

# Setup virtual enviroment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

sh scripts/setup_db.sh
