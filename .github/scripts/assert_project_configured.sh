#!/usr/bin/env bash
# Blocks CD deploy while this repo still looks like the clean_mss_template starter.
# Customize the markers below when creating a real microservice from the template.
set -euo pipefail

REPO_NAME="${GITHUB_REPOSITORY##*/}"

FORBIDDEN_REPO_NAMES=(
  "clean_mss_template"
)

FORBIDDEN_STACK_PREFIX="CleanMssTemplate"
FORBIDDEN_PROJECT_TAG="Template"

failed=0

for name in "${FORBIDDEN_REPO_NAMES[@]}"; do
  if [[ "$REPO_NAME" == "$name" ]]; then
    echo "::error::Repository is still named '${name}'. Rename it before enabling CD deploy."
    failed=1
  fi
done

if [[ "${GITHUB_REPOSITORY}" == "Maua-Dev/clean_mss_template" ]]; then
  echo "::error::Refusing to deploy the upstream template repository itself."
  failed=1
fi

if grep -qE "STACK_NAME=${FORBIDDEN_STACK_PREFIX}" .github/workflows/aws_deploy_cd.yml; then
  echo "::error::Change STACK_NAME prefix in .github/workflows/aws_deploy_cd.yml (still '${FORBIDDEN_STACK_PREFIX}')."
  failed=1
fi

if grep -qE "['\"]project['\"]: ['\"]${FORBIDDEN_PROJECT_TAG}['\"]" iac/app.py; then
  echo "::error::Change the project tag in iac/app.py (still '${FORBIDDEN_PROJECT_TAG}')."
  failed=1
fi

if [[ "$failed" -ne 0 ]]; then
  echo ""
  echo "CD deploy is blocked until the template identity is customized."
  echo "No AWS resources will be created."
  exit 1
fi

echo "Template identity looks customized. Deploy may proceed."
