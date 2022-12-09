# Helper functions for dynamo for SLS handlers

# SortKey prefix for indicating a specific metric
# IMPORTANT: This must come AFTER the digits in the ascii table
SK_CLASS_PREFIX = ":"
SK_SHARE_PREFIX = SK_CLASS_PREFIX + "SHARE#"

def query_page_index_params(table_name, user_id, sort_key_filter=None):
    params = {
        "TableName": table_name,
        # Always use the same projection for this query
        "ProjectionExpression": "UserPages,SortKey",
        "KeyConditionExpression": "UserPages = :pk",
        "ExpressionAttributeValues": { ":pk": {"S": f"{user_id}#INDEX"} }
    }

    if sort_key_filter:
        params["KeyConditionExpression"] += " AND begins_with(SortKey, :sk)"
        params["ExpressionAttributeValues"][":sk"] = { "S": f"{user_id}#{sort_key_filter}" }

    return params

def count_page_visits_params(table_name, user_id, page_id):
    return {
        "TableName": table_name,
        "Select": "COUNT",
        "KeyConditionExpression": "UserPages = :pk AND SortKey < :sk",

        # Using SK_CLASS_PREFIX gives us anything that is a number
        "ExpressionAttributeValues": { ":pk": { "S": f"{user_id}#{page_id}" }, ":sk": { "S": SK_CLASS_PREFIX }}

    }

def query_page_visits_params(table_name, user_id, page_id):
    return {
        "TableName": table_name,
        # Always use the same projection for this query
        "ProjectionExpression": "UserPages,SortKey",
        "KeyConditionExpression": "UserPages = :pk AND SortKey < :sk",
        "ExpressionAttributeValues": { ":pk": {"S": f"{user_id}#{page_id}"}, ":sk": { "S": SK_CLASS_PREFIX } },
    }
