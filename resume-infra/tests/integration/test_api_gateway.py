import os
import boto3
import pytest
import requests
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def _creds_available() -> bool:
    try:
        return boto3.Session().get_credentials() is not None
    except (NoCredentialsError, PartialCredentialsError):
        return False
    except Exception:
        return False

pytestmark = pytest.mark.skipif(
    not _creds_available(),
    reason="Integration test needs AWS credentials (skipped in PR CI)."
)

class TestApiGateway:

    @pytest.fixture()
    def api_gateway_url(self):
        """ Get the API Gateway URL from CloudFormation Stack outputs """
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")

        if stack_name is None:
            raise ValueError('Please set the AWS_SAM_STACK_NAME environment variable to the name of your stack')

        client = boto3.client("cloudformation", region_name=os.environ.get("AWS_REGION", "us-east-1"))

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name} \n"
                f'Please make sure a stack with the name "{stack_name}" exists'
            ) from e

        outputs = response["Stacks"][0]["Outputs"]

        # ✅ Make sure this matches your template.yaml OutputKey
        api_url_output = next((o for o in outputs if o["OutputKey"] == "VisitorApiBaseUrl"), None)

        if api_url_output is None:
            raise KeyError(f"VisitorApiBaseUrl not found in stack {stack_name}")

        return api_url_output["OutputValue"]  # base URL, e.g., https://xyz.execute-api.us-east-1.amazonaws.com/Prod

    def test_visitor_count_get(self, api_gateway_url):
        """ Call the /visitor-count GET endpoint and verify response """
        url = api_gateway_url
        response = requests.get(url)

        assert response.status_code == 200
        json_data = response.json()
        assert "count" in json_data
        assert isinstance(json_data["count"], int)
