.PHONY: build deploy-infra deploy-site deploy-cert deploy-cert-guided

# Build from resume-infra directory
build:
	cd resume-infra && sam build

# Deploy the infrastructure stack using the 'resume' config env
deploy-infra:
	cd resume-infra && \
	aws-vault exec my-user --no-session -- \
	sam deploy --config-env resume --debug

# Deploy the certificate stack using the 'cert' config env
deploy-cert:
	cd resume-cert && \
	aws-vault exec my-user --no-session -- \
	sam deploy --template-file cert.yaml --config-env cert

deploy-site:
	aws-vault exec my-user --no-session -- bash -c '\
	BUCKET_NAME=$$(aws cloudformation describe-stacks \
	  --stack-name cloud-resume-infra \
	  --query '\''Stacks[0].Outputs[?OutputKey==`LandingPage`].OutputValue'\'' \
	  --output text --region us-east-1); \
	echo "Deploying to $$BUCKET_NAME"; \
	aws s3 sync ./resume-site s3://$$BUCKET_NAME --delete'


# Redeploy certificate stack interactively
deploy-cert-guided:
	cd resume-cert && \
	aws-vault exec my-user --no-session -- \
	sam deploy --guided --config-env cert

# Invalidate CloudFront Cache
invalidate-cache:
	aws-vault exec my-user --no-session -- bash -c '\
	DISTRIBUTION_ID=$$(aws cloudformation describe-stacks \
	  --stack-name cloud-resume-infra \
	  --query '\''Stacks[0].Outputs[?OutputKey==`CloudFrontDistributionId`].OutputValue'\'' \
	  --output text --region us-east-1); \
	echo "Invalidating CloudFront distribution $$DISTRIBUTION_ID..."; \
	aws cloudfront create-invalidation \
	  --distribution-id $$DISTRIBUTION_ID \
	  --paths "/*"'

