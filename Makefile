.PHONY: build deploy-infra deploy-site deploy-cert deploy-cert-guided invalidate-cache

NEED_ENV_TARGETS := deploy-infra deploy-cert deploy-cert-guided
ifneq (,$(filter $(NEED_ENV_TARGETS),$(MAKECMDGOALS)))
ifndef ENV
$(error ENV is not set. Run like: make $@ ENV=prod)
endif
endif

REGION ?= us-east-1

PROFILE := $(ENV)

build:
	cd resume-infra && sam build

deploy-infra:
	cd resume-infra && \
	sam deploy \
	  --stack-name cloud-resume-infra \
	  --config-env $(ENV) \
	  --region us-east-1 \
	  --capabilities CAPABILITY_IAM \
	  --no-confirm-changeset \
	  --no-fail-on-empty-changeset

deploy-cert:
	cd resume-cert && \
	sam deploy --template-file cert.yaml --config-env cert --region $(REGION)

deploy-site:
	BUCKET_NAME=$$(aws cloudformation describe-stacks \
	  --stack-name cloud-resume-infra \
	  --query 'Stacks[0].Outputs[?OutputKey==`LandingPage`].OutputValue' \
	  --output text --region $(REGION)); \
	API_URL=$$(aws cloudformation describe-stacks \
	  --stack-name cloud-resume-infra \
	  --query 'Stacks[0].Outputs[?OutputKey==`VisitorApiBaseUrl`].OutputValue' \
	  --output text --region $(REGION)); \
	echo "Writing resume-site/config.json with API_URL=$$API_URL"; \
	printf '{ "apiBaseUrl": "%s" }\n' "$$API_URL" > resume-site/config.json; \
	echo "Deploying to $$BUCKET_NAME"; \
	aws s3 sync ./resume-site s3://$$BUCKET_NAME --delete \
	  --cache-control "no-store" \
	  --exact-timestamps \
	  --region $(REGION)

deploy-cert-guided:
	cd resume-cert && \
	sam deploy --guided --config-env cert --region $(REGION) 

invalidate-cache:
	DISTRIBUTION_ID=$$(aws cloudformation describe-stacks \
	  --stack-name cloud-resume-infra \
	  --query 'Stacks[0].Outputs[?OutputKey==`CloudFrontDistributionId`].OutputValue' \
	  --output text --region $(REGION); \
	echo "Invalidating CloudFront distribution $$DISTRIBUTION_ID..."; \
	aws cloudfront create-invalidation \
	  --distribution-id $$DISTRIBUTION_ID \
	  --paths "/*" \
	  --region $(REGION)
invalidate-cache:
	DISTRIBUTION_ID=$$(aws cloudformation describe-stacks \
	  --stack-name cloud-resume-infra \
	  --query 'Stacks[0].Outputs[?OutputKey==`CloudFrontDistributionId`].OutputValue' \
	  --output text --region $(REGION)); \
	echo "Invalidating CloudFront distribution $$DISTRIBUTION_ID..."; \
	aws cloudfront create-invalidation \
	  --distribution-id $$DISTRIBUTION_ID \
	  --paths '/*' \
	  --region $(REGION)
