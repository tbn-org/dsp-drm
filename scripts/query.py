from boto3.dynamodb.conditions import Key
import boto3
from pprint import pprint
import decimal
import json

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def deserialize_dynamodb_items(items):
    return json.loads(json.dumps(items, cls=DecimalEncoder))


dynamodb = boto3.resource('dynamodb', region_name="us-west-2")
query = f"SELECT * FROM \"AdInjectorStack-admarkers1883EE12-12D2XUK7D00SG\" WHERE mediaid=?"
output = dynamodb.meta.client.batch_execute_statement(Statements = [{"Statement":query, "Parameters":["5MyCBuss"]},{"Statement":query, "Parameters":["1BafLs9Y"]}])
pprint(output["Responses"])

# for response in output["Responses"]:
#     item = response["Item"]
#     pprint(deserialize_dynamodb_items(item))