from aws_cdk import (
    core,
    aws_dynamodb as dynamo,
    aws_lambda as lam,
    aws_apigateway as apigateway,
)

# from aws_lambda import AssetCode, Function, Runtime, Code
# from aws_apigateway import RestApi, LambdaIntegration, IResource, MockIntegration, PassthroughBehavior

class SchedulerApiTemplatePyStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        
        # DynamoDB定義
        dynamo_table = dynamo.Table(self, "schedule",
            partition_key={
                "name": "id",
                "type": dynamo.AttributeType.STRING,
            },
            table_name="schedule",
            removal_policy=core.RemovalPolicy.DESTROY, # NOT recommended for production code
        )

        # GET Request
        get_schedule_lambda = lam.Function(self, "get-schedule-function", 
            code=lam.Code.from_asset("lambda"),
            handler="get_schedule.lambda_handler",
            runtime=lam.Runtime.PYTHON_3_8,
            environment={
                "TABLE_NAME": dynamo_table.table_name,
                "PRIMARY_KEY": "id",
            },
        )
        dynamo_table.grant_read_data(get_schedule_lambda)


        # POST Request
        set_schedule_lambda = lam.Function(self, "set-schedule-function", 
            code=lam.Code.from_asset("lambda"),
            handler="set_schedule.lambda_handler",
            runtime=lam.Runtime.PYTHON_3_8,
            environment={
                "TABLE_NAME": dynamo_table.table_name,
                "PRIMARY_KEY": "id",
            },
        )
        dynamo_table.grant_read_write_data(set_schedule_lambda)

        api = apigateway.RestApi(self, "scheduler-api-template",
            rest_api_name="scheduler-api-template"
        )

        schedule = api.root.add_resource("schedule")
        schedule.add_resource("{id}").add_method("GET", apigateway.LambdaIntegration(get_schedule_lambda))
        # schedule.add_method("GET", apigateway.LambdaIntegration(get_schedule_lambda))
        schedule.add_method("POST", apigateway.LambdaIntegration(set_schedule_lambda))
        add_cors_options(schedule)
    
def add_cors_options(api_resource: apigateway.IResource):
    api_resource.add_method(
        "OPTIONS",
        apigateway.MockIntegration(
            integration_responses=[
                {
                    "statusCode": "200",
                    "responseParameters": {
                        "method.response.header.Access-Control-Allow-Headers":
                        "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent'",
                        "method.response.header.Access-Control-Allow-Origin": "'*'",
                        "method.response.header.Access-Control-Allow-Credentials":
                        "'false'",
                        "method.response.header.Access-Control-Allow-Methods":
                        "'OPTIONS,GET,PUT,POST,DELETE'",
                    },
                },
            ],
            passthrough_behavior=apigateway.PassthroughBehavior.NEVER,
            request_templates={
                "application/json": '{"statusCode": 200}',
            },
        ),
        method_responses=[
            {
                "statusCode": "200",
                "responseParameters": {
                    "method.response.header.Access-Control-Allow-Headers": True,
                    "method.response.header.Access-Control-Allow-Methods": True,
                    "method.response.header.Access-Control-Allow-Credentials": True,
                    "method.response.header.Access-Control-Allow-Origin": True,
                },
            },
        ],
    )