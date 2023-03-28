import json

from src.modules.create_user.app.create_user_presenter import lambda_handler


class Test_CreateUserPresenter:

    def test_create_user(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
            "cookies": [
                "cookie1",
                "cookie2"
            ],
            "headers": {
                "header1": "value1",
                "header2": "value1,value2"
            },
            "queryStringParameters": {
                "parameter1": "1"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "authentication": None,
                "authorizer": {
                    "iam": {
                        "accessKey": "AKIA...",
                        "accountId": "111122223333",
                        "callerId": "AIDA...",
                        "cognitoIdentity": None,
                        "principalOrgId": None,
                        "userArn": "arn:aws:iam::111122223333:user/example-user",
                        "userId": "AIDA..."
                    }
                },
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "domainPrefix": "<url-id>",
                "external_interfaces": {
                    "method": "POST",
                    "path": "/my/path",
                    "protocol": "HTTP/1.1",
                    "sourceIp": "123.123.123.123",
                    "userAgent": "agent"
                },
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "body": '{"name":"EhOLudjas",  "email":"eho@ludjas.com"}',
            "pathParameters": None,
            "isBase64Encoded": None,
            "stageVariables": None
        }

        # event = {'body': '{\r\n'
        #                  '    "name": "Bruno Soller Da Silva",\r\n'
        #                  '    "email": "sollinhp@soller.com"\r\n'
        #                  '}',
        #          'headers': {'Accept': '*/*',
        #                      'Accept-Encoding': 'gzip, deflate, br',
        #                      'Connection': 'keep-alive',
        #                      'Content-Length': '78',
        #                      'Content-Type': 'application/json',
        #                      'Host': '127.0.0.1:3000',
        #                      'Postman-Token': 'b7ecf13d-9745-4059-80c8-3f93cee693c0',
        #                      'User-Agent': 'PostmanRuntime/7.29.2',
        #                      'X-Forwarded-Port': '3000',
        #                      'X-Forwarded-Proto': 'http'},
        #          'httpMethod': 'POST',
        #          'isBase64Encoded': False,
        #          'multiValueHeaders': {'Accept': ['*/*'],
        #                                'Accept-Encoding': ['gzip, deflate, br'],
        #                                'Connection': ['keep-alive'],
        #                                'Content-Length': ['78'],
        #                                'Content-Type': ['application/json'],
        #                                'Host': ['127.0.0.1:3000'],
        #                                'Postman-Token': ['b7ecf13d-9745-4059-80c8-3f93cee693c0'],
        #                                'User-Agent': ['PostmanRuntime/7.29.2'],
        #                                'X-Forwarded-Port': ['3000'],
        #                                'X-Forwarded-Proto': ['http']},
        #          'multiValueQueryStringParameters': None,
        #          'path': '/mss-template/create-user',
        #          'pathParameters': None,
        #          'queryStringParameters': None,
        #          'requestContext': {'accountId': '123456789012',
        #                             'apiId': '1234567890',
        #                             'domainName': '127.0.0.1:3000',
        #                             'extendedRequestId': None,
        #                             'httpMethod': 'POST',
        #                             'identity': {'accountId': None,
        #                                          'apiKey': None,
        #                                          'caller': None,
        #                                          'cognitoAuthenticationProvider': None,
        #                                          'cognitoAuthenticationType': None,
        #                                          'cognitoIdentityPoolId': None,
        #                                          'sourceIp': '127.0.0.1',
        #                                          'user': None,
        #                                          'userAgent': 'Custom User Agent String',
        #                                          'userArn': None},
        #                             'path': '/mss-template/create-user',
        #                             'protocol': 'HTTP/1.1',
        #                             'requestId': 'c75adc38-5577-4c83-871a-6001f2b06b43',
        #                             'requestTime': '03/Feb/2023:02:30:59 +0000',
        #                             'requestTimeEpoch': 1675391459,
        #                             'resourceId': '123456',
        #                             'resourcePath': '/mss-template/create-user',
        #                             'stage': 'prod'},
        #          'resource': '/mss-template/create-user',
        #          'stageVariables': None,
        #          'version': '1.0'}

        response = lambda_handler(event, None)

        assert response["statusCode"] == 201
        assert json.loads(response["body"])["message"] == "the user was created successfully"
