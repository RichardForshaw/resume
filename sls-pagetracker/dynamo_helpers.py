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

def query_page_visits_params(table_name, user_id, page_id, from_ts=None, to_ts=None):
    cond_expr = "< :sk_to"
    from_key = {}
    to_key = {":sk_to": { "S": SK_CLASS_PREFIX }}
    if from_ts:
        cond_expr = "BETWEEN :sk_from AND :sk_to"
        from_key = {':sk_from': { "S": str(from_ts)}}
    if to_ts:
        to_key = {":sk_to": { "S": str(to_ts) }}

    return {
        "TableName": table_name,
        # Always use the same projection for this query
        "ProjectionExpression": "UserPages,SortKey",
        # Alter the expression based on the filter arguments
        "KeyConditionExpression": f"UserPages = :pk AND SortKey {cond_expr}",
        "ExpressionAttributeValues": { ":pk": {"S": f"{user_id}#{page_id}"}} | to_key | from_key,
    }
