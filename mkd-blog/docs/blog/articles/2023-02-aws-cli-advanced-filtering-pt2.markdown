---
layout: post
title:  "AWS CLI JSON Filtering Part 2: An Advanced Example"
description: "Part 2 of learning advanced JSON filtering with JMES and JQ. This post runs through an example of re-structuring output from a CLI SQL query to insert directly into DynamoDB."
tags:
    - Cloud Development
    - AWS
    - CLI
    - Bash
    - JSON
    - DynamoDB
author: Richard Forshaw
---

In the [previous post](./2023-02-aws-cli-advanced-filtering.markdown), I introduced how you can query, filter and re-structure JSON using both the JSON/JMES parsing function built-in to the CLI or the JQ tool. The examples in the first post may be enough for you to get more out of your CLI responses, but we can do much much more.

In this post I look at how to put it all together to tackle an interesting real-world example, perhaps saving you many lines of code. These tools effectively offer a mini-programming-language, and when combined with a powerful shell like bash, amazing things can be achieved without resorting to writing small scripts in your favourite language.

If you want to see how you can use JMES/JQ to transform database output and then _feed in to_ another AWS service, then read on!

![JSON Pipeline](./images/JSON_pipeline.png)

## Your own JSON ETL pipeline

Let's revisit the fact that you can query S3 log files using queries stored in AWS Athena (see [this post](./2023-01-web-analytics-3-ways.markdown)). Let's say that you have built a DynamoDB table to track your page visits, and you want to populate it with the historical data that you already have in the S3 logs. Your first thought might be to download all the S3 data and write a small parsing program to push the data into Dynamo. Well, what if you can query Athena and then _construct DynamoDB data without writing any code_. Just using text manipulation.

I'll use this as an example to show a practical way to generate data from Athena that you can then use to populate DynamoDB. I could use another database or tool which outputs JSON, but I chose Athena because:

 - I have visited it before and it ties into the theme of this blog
 - It can be queried using the AWS CLI tool, which means we can flex our JMES skills
 - The querying process involves several steps, so it provides a good example of passing output down a command chain

*Warning*: The post ahead contains some features provided by bash, such as piping and the `tr` and `xargs` commands. Don't be scared...

We will limit ourselves here to populating DynamoDB with the current historical visit counts to each page, which we already have an Athena query for. We will use both JSON querying methods - first let's get started with the AWS JMES filter.

### Getting the query

Athena lets you store 'named queries' that you can access again and again from the CLI, but it is a bit annoying in that it doesn't easily show you any details of your stored queries. Instead you have to batch-query each of the IDs. But how do you know what the IDs are? That's easy...

```
bash-5.1$ aws athena list-named-queries
{
    "NamedQueryIds": [
        "1bcd8fa9-e6ca-477d-9a72-3b02fc4b34ef",
        "09f659cd-2a59-49be-977e-cee283e3ee11"
    ]
}
```

The `athena batch-get-named-query` function takes a list of IDs, so we can use our new knowledge and a new function `join` to convert this into a space-separated string. Note that `join` takes a special argument `@` which I will not elaborate on here - go and look at the manual!

```
bash-5.1$ aws athena list-named-queries --query "NamedQueryIds | join(' ', @)" | tr -d '"'
1bcd8fa9-e6ca-477d-9a72-3b02fc4b34ef 09f659cd-2a59-49be-977e-cee283e3ee11
```

Note that we needed a special bash-command `tr -d '"'` because the CLI output presents strings wrapped in quotes and we don't want that.

The `batch-get-named-query` command returns output like this:

```
{
    "NamedQueries": [
        {
            "Name": "pagetotals",
            "Database": "s3_access_logs_db",
            "QueryString": "SELECT FROM MyTable...",
            "NamedQueryId": "1bcd8fa9-e6ca-477d-9a72-3b02fc4b34ef",
            "WorkGroup": "primary"
        },
        ...
    ]
}
```

So, with the power of JMES and bash back-quoting, we get:

```
bash-5.1$ aws athena batch-get-named-query --named-query-ids `aws athena list-named-queries --query "NamedQueryIds | join(' ', @)" | tr -d '"'` --query "NamedQueries[?Name=='pagetotals'].QueryString | [0]"
"SELECT FROMMyTable..."
```

OK great. So now we need to execute it. It is a bit cumbersome to be nesting commands over and over, so we can turn to our trusty friend `xargs`, which passes the output to the end of the next command. Thus the above example becomes:

```
bash-5.1$ aws athena list-named-queries --query "NamedQueryIds | join(' ', @)" \
> | tr -d '"' \
> | xargs aws athena batch-get-named-query --query "NamedQueries[?Name=='pagetotals'].QueryString | [0]" \
> --named-query-ids
"SELECT FROM MyTable..."
```

Now that this piping makes constructing a command easier, we can pass this output into the final command. We can also use the line-continuation character `\` to format it nicer.

```
bash-5.1$ aws athena list-named-queries --query "NamedQueryIds | join(' ', @)" \
> | tr -d '"' \
> | xargs aws athena batch-get-named-query --query "NamedQueries[?Name=='pagetotals'].QueryString | [0]" \
> --named-query-ids \
> | xargs aws athena start-query-execution --work-group primary --query-string
--------------------------------------------------------------
|                     StartQueryExecution                    |
+-------------------+----------------------------------------+
|  QueryExecutionId |  cf41ddc4-076f-4e3d-bd4d-aa52e9802402  |
+-------------------+----------------------------------------+
```

And the query is running!

This seems to be a bit of a cumbersome command, but it does show how the output can be formatted to be passed to a sequence of commands. The command could be aliased with a parameter to retrieve any named query's SQL data by its name instead of its ID.

![Transforming](./images/Transformer-Converting.jpg)

### Transforming the Results

Now let's parse the results. When we get the results back from Athena, the structure looks like this:

```
{
    "ResultSet": {
        "Rows": [
            {
                "Data": [
                    { "VarCharValue": "_col0" },
                    { "VarCharValue": "_col1" }
                ]
            },
            {
                "Data": [
                    { "VarCharValue": "blog/articles/2022-09-08-productivity-and-agile/"},
                    { "VarCharValue": "173" }
                ]
            },
            {
                "Data": [
                    { "VarCharValue": "blog/articles/2022-12-Scrum-Misconceptions/" },
                    { "VarCharValue": "77" }
                ]
            },
            ...
        ]
    },
    ...
}
```

For simplicity, say this is stored in a local file. Let's switch over to JQ to parse the results. We want to insert this data into Dynamo, so we need it in the following form:

```
{
    'PrimaryKey': {'S': 'Value'},
    'SortKey': {'S': 'Value'},
    'AttributeN': {'N': Value},
    ...
}
```

Since we know the `PrimaryKey` and `SortKey` (we should know this because of our schema), we need to turn each of the `Data` values in the Athena results into a `key:value` pair. Let's give it a go. In JQ we can construct objects as well using the `{}` operator, so the result is something like this (note the outer quotes allows you to break the lines):

```
bash-5.1$ jq '
> [{PrimaryKey: {S: "PKVal"}}, {SortKey: {S: "SKVal"}}] + [.ResultSet.Rows[1:][]
> | {(.Data[0].VarCharValue): {N: .Data[1].VarCharValue}}]
> | add' athena.json
{
  "PrimaryKey": { "S": "PKVal" },
  "SortKey": { "S": "SKVal" },
  "blog/articles/2022-09-08-productivity-and-agile/": { "N": "173" },
  "blog/articles/2022-12-Scrum-Misconceptions/": { "N": "77" },
  ...
}
```

More important to note here is the quoting - when constructing objects the key does not need quotes but the value does, if using strings. If using expressions then the key needs parentheses `()` but the value needs nothing. Lets break down the whole expression.

| JQ Expression     |  Meaning  |
|-|-|
| `[{PrimaryKey: {S: "PKVal"}}, {SortKey: {S: "SKVal"}}]` | This is the hard-coded values of the data, because we already know where we want to insert this data |
| `+` | In this context, `+` is for concatenation of arrays |
| `[...]` | The outer `[]` of the next section mean that we want the output wrapped in an array |
| `.ResultSet.Rows[1:][] |` | Take everything from the second element of `ResultSet.Rows` and pass it to the next step (we discard the first item because it does not have useful data) |
| `{(.Data[0].VarCharValue): {N: .Data[1].VarCharValue}}` | Construct an object of structure `{X: {"N": Y}}` from each item received. Evaluate the first value into the key name, and take the second as the value |
| `| add` | Because the expression until now outputs a list of object, passing the list to `add` constructs one object (i.e. add all the objects in the list together) |


### Push into DynamoDb

From here you can actually insert this straight into DynamoDB! We need to re-visit our friend `xargs`:

```
bash-5.1$jq -r '
> [{PrimaryKey: {S: "PKVal"}}, {SortKey: {S: "SKVal"}}] + [.ResultSet.Rows[1:][]
> | {(.Data[0].VarCharValue): {N: .Data[1].VarCharValue}}]
> | add | tostring' athena.json \
> | xargs -I jsondata aws dynamodb put-item --table-name MyTable --item 'jsondata'
```

A quick breakdown:

 - `jq -r` asks jq to output raw text, which we need in order to pass our output into the AWS CLI command correctly
 - the jq `tostring` function causes jq to format the resulting JSON as a string, which we also need in order to pass to the AWS CLI command correctly
 - `xargs -I jsondata` causes xargs to replace the keyword `jsondata` with the output that it received from the preceding command
 - therefore when we use `aws dynamodb ... --item 'jsondata'`, the `jsondata` is replaced with our actual JSON, which has been correctly quoted.

You can always run this command bit-by-bit to see it in action.

## Conclusion

I hope I have demonstrated that with a little knowledge, you can replace potentially dozens of lines of scripting code with some SQL queries and JSON querying. In fact, because JQ can read your filter expression from a file (which can be commented), the above examples do become 1-liners, with jq as your script interpreter:

`jq -r -f filter.jq athena.json | xargs -I jsondata aws dynamodb put-item --table-name MyTable --item 'jsondata'`

This also means that you can version-control and track your JQ scripts.

