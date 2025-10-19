#!/bin/bash
cd /home/kavia/workspace/code-generation/site-verification-and-workflow-management-system-176390-176400/backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

