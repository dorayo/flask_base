source venv/bin/activate
echo "Running tests in $(pwd)"

pytest --cov=app --cov-report=term-missing --cov-branch tests/test*
deactivate
