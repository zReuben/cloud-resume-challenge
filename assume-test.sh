#!/bin/bash

# Assume role into reuben-eng from reuben-mgmt-admin
CREDS=$(aws sts assume-role \
  --role-arn arn:aws:iam::515275665162:role/OrgAccessRole \
  --role-session-name reuben-eng-session \
  --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]' \
  --output text)

if [[ -z "$CREDS" || $(echo "$CREDS" | wc -w) -ne 3 ]]; then
  echo "❌ Failed to assume role into reuben-eng. Check permissions or MFA config."
  return 1
fi

export AWS_ACCESS_KEY_ID=$(echo "$CREDS" | cut -f1)
export AWS_SECRET_ACCESS_KEY=$(echo "$CREDS" | cut -f2)
export AWS_SESSION_TOKEN=$(echo "$CREDS" | cut -f3)

echo "✅ Assumed role into reuben-eng"

