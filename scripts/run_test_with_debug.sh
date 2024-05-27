source venv/bin/activate
echo "Running tests in $(pwd)"

pytest -s --cov=app --cov-report=term-missing --cov-branch tests/test*
deactivate
