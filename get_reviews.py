import boto3


# script to query dynamodb table based on business_name and output a text file that has a line for each 'text' attribute in the record
def query_business(business_name):
    ddb_client = boto3.client("dynamodb", region_name="us-west-1")
    response = ddb_client.query(
        TableName="business_review",
        KeyConditionExpression="business_name = :business_name",
        ExpressionAttributeValues={":business_name": {"S": business_name}},
        # use the GSI business_name_index to speed up the query
        IndexName="business_name-index",
    )
    # print(response)
    text = ""
    for i, item in enumerate(response["Items"]):
        text += f"Review {i}: {item['text']['S']}\n\n"

    with open(business_name + ".txt", "w") as f:
        f.write(text)


# main function that takes the business_name as an input and runs the query_business function
def main():
    business_name = input("Enter the business name: ")
    query_business(business_name)


if __name__ == "__main__":
    main()