
from dynamo_helpers import *
from datetime import datetime

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

def test_query_page_counters():
    expected = {
        "TableName": "Table",
        "KeyConditionExpression": "UserPages = :pk AND begins_with(SortKey, :sk)",
        "ExpressionAttributeValues": { ":pk": {"S": "UserID"}, ":sk": {"S": "PAGES#"}},
    }

    assert query_page_counters_params("Table", "UserID") == expected

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
        "KeyConditionExpression": "UserPages = :pk AND SortKey < :sk_to",
        "ExpressionAttributeValues": { ":pk": {"S": f"UserID#PageID"}, ":sk_to": {"S": ":"} },
    }

    assert query_page_visits_params("Table", "UserID", "PageID") == expected

def test_query_page_visits_with_from_time():
    expected = {
        "TableName": "Table",
        "ProjectionExpression": "UserPages,SortKey",
        "KeyConditionExpression": "UserPages = :pk AND SortKey BETWEEN :sk_from AND :sk_to",
        "ExpressionAttributeValues": { ":pk": {"S": f"UserID#PageID"}, ":sk_from": {"S": "12345"}, ":sk_to": {"S": ":"} },
    }

    assert query_page_visits_params("Table", "UserID", "PageID", from_ts=12345) == expected

def test_query_page_visits_with_to_time():
    expected = {
        "TableName": "Table",
        "ProjectionExpression": "UserPages,SortKey",
        "KeyConditionExpression": "UserPages = :pk AND SortKey < :sk_to",
        "ExpressionAttributeValues": { ":pk": {"S": f"UserID#PageID"}, ":sk_to": {"S": "12345"} },
    }

    assert query_page_visits_params("Table", "UserID", "PageID", to_ts=12345) == expected

def test_query_page_visits_with_from_time_and_to_time():
    expected = {
        "TableName": "Table",
        "ProjectionExpression": "UserPages,SortKey",
        "KeyConditionExpression": "UserPages = :pk AND SortKey BETWEEN :sk_from AND :sk_to",
        "ExpressionAttributeValues": { ":pk": {"S": f"UserID#PageID"}, ":sk_from": {"S": "12345"}, ":sk_to": {"S": "54321"} },
    }

    assert query_page_visits_params("Table", "UserID", "PageID", from_ts=12345, to_ts=54321) == expected

def test_update_page_totals_counter():
    expected = {
        "TableName": "Table",
        "Key": {"UserPages": {"S": "UserID"}, "SortKey": {"S": "PAGES#202201"}},
        "UpdateExpression": "ADD #page :incr",
        "ExpressionAttributeNames": {"#page": "PageID"},
        "ExpressionAttributeValues": {":incr": {"N": "1"}}
    }

    test_timestamp = int(datetime(2022,1,5,6,7).timestamp())
    assert update_page_totals_counter_params("Table", "UserID", "PageID", test_timestamp) == expected

def test_update_page_totals_counter_with_list():
    expected = {
        "TableName": "Table",
        "Key": {"UserPages": {"S": "UserID"}, "SortKey": {"S": "PAGES#202201"}},
        "UpdateExpression": "ADD #page :incr",
        "ExpressionAttributeNames": {"#page": "PageID"},
        "ExpressionAttributeValues": {":incr": {"N": "2"}}
    }

    test_timestamp = int(datetime(2022,1,5,6,7).timestamp())
    assert update_page_totals_counter_params("Table", "UserID", "PageID", [test_timestamp,]*2) == expected

def test_update_page_visits_counter():
    expected = {
        "TableName": "Table",
        "Key": {"UserPages": {"S": "UserID#PageID"}, "SortKey": {"S": "VISITS#202201"}},
        "UpdateExpression": "ADD #day :incr",
        "ExpressionAttributeNames": {"#day": "D05"},
        "ExpressionAttributeValues": {":incr": {"N": "1"}}
    }

    test_timestamp = int(datetime(2022,1,5,6,7).timestamp())
    assert update_page_visits_counter_params("Table", "UserID", "PageID", test_timestamp) == expected

def test_update_page_visits_counter_with_list():
    expected = {
        "TableName": "Table",
        "Key": {"UserPages": {"S": "UserID#PageID"}, "SortKey": {"S": "VISITS#202201"}},
        "UpdateExpression": "ADD #day :incr",
        "ExpressionAttributeNames": {"#day": "D05"},
        "ExpressionAttributeValues": {":incr": {"N": "3"}}
    }

    test_timestamp = int(datetime(2022,1,5,6,7).timestamp())
    assert update_page_visits_counter_params("Table", "UserID", "PageID", [test_timestamp,]*3) == expected

