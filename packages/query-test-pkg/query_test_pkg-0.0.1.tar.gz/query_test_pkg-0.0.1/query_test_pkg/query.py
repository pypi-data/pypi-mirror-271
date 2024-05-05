import os
import json
import boto3


class MyQueryClass:
    def __init__(self):
        self.db_table = self._initialize_dynamodb_table()

    def _initialize_dynamodb_table(self):
        table_name = os.environ.get("PLUTO_DYNAMODB_TABLE_QUERY", "query-table")
        dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
        return dynamodb.Table(table_name)

    def put_item(self, Item):
        """
        Insert an item to table
        """
        res = self.db_table.put_item(Item=Item)
        print(f"response from creating item - {res}")
        status_code = res.get("ResponseMetadata", {}).get("HTTPStatusCode")
        return status_code

    def list_item(self):
        """
        Get list of Item
        """
        res = self.db_table.scan()
        print(f"res from list item - {res}")
        item_response = res.get("Items", [])
        print(f"response from list item - {item_response}")
        status_code = res.get("ResponseMetadata", {}).get("HTTPStatusCode")
        return status_code

    def descibe(self, query_id):
        """
        Get an Item from table
        """
        key = {"QueryId": query_id}
        res = self.db_table.get_item(Key=key)
        status_code = res.get("ResponseMetadata", {}).get("HTTPStatusCode")
        return status_code

    def update_item(self, query_id, update_mask):
        """
        Update an Item
        """
        res = self.db_table.update_item(
            Key={"QueryId": query_id},
            UpdateExpression="SET #data = :data",
            ExpressionAttributeNames={"#data": "Data"},
            ExpressionAttributeValues={":data": update_mask},
        )
        status_code = res.get("ResponseMetadata", {}).get("HTTPStatusCode")
        return status_code

    def delete_item(self, query_id):
        """
        Delete an Item
        """
        res = self.db_table.delete_item(Key={"QueryId": query_id})
        status_code = res.get("ResponseMetadata", {}).get("HTTPStatusCode")
        return status_code
