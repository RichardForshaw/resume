# Helper functions for dynamo for SLS handlers

from datetime import datetime

# SortKey prefix for indicating a specific metric
# IMPORTANT: This must come AFTER the digits in the ascii table
SK_PAGE_COUNT_KEY = "PAGES"
SK_PAGE_VISITS_KEY = "VISITS"
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

def query_page_counters_params(table_name, user_id):
    ''' Query for the access counters of the pages '''
    return {
        "TableName": table_name,
        "KeyConditionExpression": "UserPages = :pk AND begins_with(SortKey, :sk)",
        "ExpressionAttributeValues": { ":pk": { "S": user_id }, ":sk": { "S": SK_PAGE_COUNT_KEY + "#" }}
    }

def count_page_visits_params(table_name, user_id, page_id):
    return {
        "TableName": table_name,
        "Select": "COUNT",
        "KeyConditionExpression": "UserPages = :pk AND SortKey < :sk",

        # Using SK_CLASS_PREFIX gives us anything that is a number
        "ExpressionAttributeValues": { ":pk": { "S": f"{user_id}#{page_id}" }, ":sk": { "S": SK_CLASS_PREFIX }}

    }

def query_page_visits_params(table_name, user_id, page_id, from_month=None, to_month=None):
    cond_expr = "begins_with(SortKey, :sk)"
    from_key = {}
    to_key = {":sk": { "S": SK_PAGE_VISITS_KEY + "#" }}

    # User provides parameters
    if from_month or to_month:
        # Use a BETWEEN expression. Set up the keys to handle the SortKey limits
        cond_expr = "SortKey BETWEEN :sk_from AND :sk_to"

        # Use "#0" as lower limit because it will capture all greater numbers
        from_key = {':sk_from': { "S": f"{SK_PAGE_VISITS_KEY}#{from_month or 0}"}}

        # Use "#MAX" as upper limit because it will capture all numbers and is a meaningful word
        to_key = {":sk_to": { "S": f"{SK_PAGE_VISITS_KEY}#{to_month or 'MAX'}" }}

    return {
        "TableName": table_name,
        # Alter the expression based on the filter arguments
        "KeyConditionExpression": f"UserPages = :pk AND {cond_expr}",
        "ExpressionAttributeValues": { ":pk": {"S": f"{user_id}#{page_id}"}} | to_key | from_key,
    }

def update_page_totals_counter_params(table_name, user_id, page_id, timestamps):
    # update the total visits for a page
    count = 1

    # Account for a list of timestamps
    if isinstance(timestamps, list):
        count = len(timestamps)
        timestamps = timestamps[0]

    dt = datetime.fromtimestamp(timestamps)
    YYYYMM = dt.strftime("%Y%m")

    return {
        "TableName": table_name,
        "Key": {"UserPages": {"S": user_id}, "SortKey": {"S": f"{SK_PAGE_COUNT_KEY}#{YYYYMM}"}},
        "UpdateExpression": "ADD #page :incr",
        "ExpressionAttributeNames": {"#page": page_id},
        "ExpressionAttributeValues": {":incr": {"N": str(count)}}
    }

def update_page_visits_counter_params(table_name, user_id, page_id, timestamps):
    ''' Update the daily page visits counter.
       'timestamps' can be a single int or a list. If a list then the counter is updated
       according to the length of the list but for the first timestamp (the function does not cater
       for updating multiple attributes)
    '''
    count = 1

    # Account for a list of timestamps
    if isinstance(timestamps, list):
        count = len(timestamps)
        timestamps = timestamps[0]

    dt = datetime.fromtimestamp(timestamps)
    YYYYMM = dt.strftime("%Y%m")
    DD = dt.strftime("D%d")

    return {
        "TableName": table_name,
        "Key": {"UserPages": {"S": f"{user_id}#{page_id}"}, "SortKey": {"S": f"{SK_PAGE_VISITS_KEY}#{YYYYMM}"}},
        "UpdateExpression": "ADD #day :incr",
        "ExpressionAttributeNames": {"#day": DD},
        "ExpressionAttributeValues": {":incr": {"N": str(count)}}
    }
