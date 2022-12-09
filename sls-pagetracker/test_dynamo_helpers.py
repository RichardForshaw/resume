
from dynamo_helpers import *

def test_query_page_index():
    expected = {
        "TableName": "Table",
        "ProjectionExpression": "UserPages,SortKey",
        "KeyConditionExpression": "UserPages = :pk",
        "ExpressionAttributeValues": { ":pk": {"S": "UserID#INDEX"} }
    }

    assert query_page_index_params("Table", "UserID") == expected

def test_query_page_index_with_page_filter():
    expected = {
        "TableName": "Table",
        "ProjectionExpression": "UserPages,SortKey",
        "KeyConditionExpression": "UserPages = :pk AND begins_with(SortKey, :sk)",
        "ExpressionAttributeValues": { ":pk": {"S": "UserID#INDEX"}, ":sk": {"S": "UserID#blog/url/" } }
    }

    assert query_page_index_params("Table", "UserID", "blog/url/") == expected

def test_count_page_visits():
    expected = {
        "TableName": "Table",
        "Select": "COUNT",
        "KeyConditionExpression": "UserPages = :pk AND SortKey < :sk",
        "ExpressionAttributeValues": { ":pk": {"S": "UserID#PageID"}, ":sk": {"S": ":"}},
    }

    assert count_page_visits_params("Table", "UserID", "PageID") == expected

def test_query_page_visits():
    expected = {
        "TableName": "Table",
        "ProjectionExpression": "UserPages,SortKey",
        "KeyConditionExpression": "UserPages = :pk AND SortKey < :sk",
        "ExpressionAttributeValues": { ":pk": {"S": f"UserID#PageID"}, ":sk": {"S": ":"} },
    }

    assert query_page_visits_params("Table", "UserID", "PageID") == expected
