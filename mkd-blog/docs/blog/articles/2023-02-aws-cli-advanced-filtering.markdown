---
layout: post
title:  "AWS CLI JSON: Advanced Filtering Techniques"
description: "After interacting more often with AWS, and especially its JSON output, I found I needed more tools in my toolbox than just the essentials. This post dives into some advanced techniques that you may find useful when dealing with your own projects."
tags:
    - Cloud Development
    - AWS
    - CLI
    - JSON
author: Richard Forshaw
---

Last year I published [AWS CLI and Docker Essentials](./2022-08-30-aws-cli-essentials.markdown), which was intended to get most people up and running, or possibly easily re-visiting their AWS cloud projects. After doing that for a few months, I found I was starting to use more advanced tools to deal with AWS, especially the JSON output.

I am a self-professed want-to-be keyboard-wizard, and I was brought up on amazing text-manipulation tools like grep, sed and awk. I have used awk to solve many problems involving text-files, and have been known to perform code-refactoring using sed, back before regular-expression support in visual editors improved.

Text-based data manipulation can still be very fast and powerful and might save you dozens of lines of code. This post shows some of the more advanced things you can do to help deal with AWS, and perhaps other cloud providers or function output which generates JSON.

This article is presented in two parts: firstly there is a gradual introduction from simple field-filtering of CLI output up to performing basic data aggregation and sorting on CLI output and other JSON structures; The second part presents an example of how you can populate a DynamoDB table with output from an Athena SQL query using only the command line. Feel free to read as far as you want.

## Tools

The tools used in this article are as follows:

 - AWS CLI
 - JMES Path parser
 - JQ
 - Bash

This combination may mean that some examples below may not map exactly to your particular use-case or configuration, so please bear that in mind.

![JSON Header](./images/JSON_header.jpg)

## Basic JSON Formatting and Filtering

I looked at basic formatting and filtering in my [AWS CLI essentials post](./2022-08-30-aws-cli-essentials.markdown). As a quick recap, you can use the `--query` command-line parameter to pass a string specifying a query expression on the JSON results, and sometimes these can get quite complex.

If you want a bit more power in your querying, it is worth looking at the [JQ tool](https://stedolan.github.io/jq/manual/), which also lets you process JSON structures. The good thing about using JQ is that if can operate on files as well as STDIN, so you can save your JSON output into a file and run JQ over and over. This will definitely be faster when writing your queries and may also save you some AWS processing cost.

As a start, JQ is great for simply pretty-formatting JSON output from something like a lambda function, by just piping it into `jq '.'`. This isn't necessary with the AWS CLI because it already formats the JSON output.

### AWS CLI examples

The simplest use of the CLI filter is to print a reduced amount of data so that it is more manageable. This uses [JMES Path expressions](https://jmespath.org/tutorial.html) to process the JSON data in the output.

Here are some basic examples. Note that the query expression is added using the `--query` argument. In this case we will use CloudFormation output:

`aws cloudformation describe-stacks --query "<filter-goes-here>"`

| Use Case                    | Command                     |
------------------------------|-----------------------------
| Show only stack ID, name and update time | `'Stacks[*].[StackId, StackName, LastUpdatedTime]'` |
| Show stack name/ID for stacks whose name contains 'foo' | `'Stacks[?StackId.contains(@, 'foo')].[StackId, StackName]'` |
| Show stack name/ID for stacks which have outputs exported *and* have been updated since Nov 2022 |  `"Stacks[?Outputs && LastUpdatedTime>'2022-11'].[StackId,StackName,LastUpdatedTime]"` |

(Note the final example only works because the date format in `LastUpdatedTime` is able to be compared as a string - more on that later.)

### JQ Examples

If you want to do serious local-processing of AWS or any other JSON output, you need to get familiar with [JQ](https://stedolan.github.io/jq/manual/), an awesome tool which lets you process JSON structures, not only filtering it like the AWS CLI, but also restructuring it.

Here are a few basic ways to use it. Note that you can either pipe input into JQ or provide a filename which contains your JSON.

| Use Case                    | Command                     |
------------------------------|-----------------------------
| Simply pretty-print JSON output | `jq '.'`                |
| Get all the sort keys from a dynamo query response <br>(assuming they are strings)| `jq '.Items[].SortKey.S'` |
| Put the result into a list  | `jq '[.Items[].SortKey.S]'` |
| Only print keys, not values | `jq 'keys[]'`               |

### An Important Note

It should be stressed here that **QUOTING IS IMPORTANT**. You may have noticed above that for the AWS `--query` I used double-quotes to enclose the whole expressions, and single-quotes when quoting literals within the expression. But for JQ, you use the opposite, which is made clear [in the manual](https://stedolan.github.io/jq/manual/#Invokingjq). At least within the environment I am using (bash), _not following this will only lead to endless miserable debugging_. So please use the quoting as you see it here, and if you get any errors, check your quotes.

## Comparing The Two

In general, the `--query` filters using JMES are a little more concise than their JQ alternatives, but in my opinion the sequential nature of JQ using pipes (`|`) is more readable than JMES. However, there are some other important differences to consider:

|             |  CLI --query expression           | JQ Expression           |
|-|-|-|
| Usage       | Only with AWS CLI commands      | With any output or file |
| Output      | Only outputs filtered results   | Can restructure and assign into JSON |
| Types       | Does not handle dates natively  | Handles date conversions |
| Scripting   | Expression must be entered on command-line | Expression can be store in file with comments |

Below are some common queries I've used, with the CLI query and JQ query side-by-side. You should note that all the JQ expressions are wrapped in `[]`, because by default JQ does not output a list. The AWS CLI query function does output a list, so the additional `[]` are used to match the outputs. For these examples, I am using DynamoDB output which looks something like this:

```
{
    "Items": [
        {
            "PartitionKey": { "S": "blog/books/2023-01-drive-daniel-pink/" },
            "SortKey": { "S": "1675071762" },
            "SomeField": { "N": "54" },
            // Other Fields...
        },
        {
            "PartitionKey": { "S": "blog/books/2023-01-drive-daniel-pink/" },
            "SortKey": { "S": "1675071862" },
            "SomeField": { "N": "44" },
            // Other Fields...
        },
        // More items...
    ]
}
```

| Example          | AWS CLI query expression          | JQ Expression             |
|-|-|-|
| Show all sort keys from dynamo output | `Items[*].SortKey.S` | `[.Items[].SortKey.S]`  |
| Particular attributes from dynamo output | `Items[*].[SortKey.S,SomeField.N]` | `[.Items[] | [.SortKey.S,.SomeField.N]]` |
| Filter by field value | `Items[?SortKey.S>'1674000000'].SomeField.N` | `[.Items[] | select(.SortKey.S>"1674000000").SomeField.N]`
| Filter on string prefix      | `Items[?starts_with(SortKey.S, 'TEXT')].SomeField.N` | `[.Items[] | select(.SortKey.S | startswith("TEXT")).SomeField.N]` |

_Note these are for example only! When using DynamoDB, you would typically use a dynamo query or projection expression instead of a client-side query_

If you want an example not using the data above, here is one you can run on your CloudFormation stacks right now, to only find the last updated time of your 'Dev'-stage stacks:

```
bash-5.1$ aws cloudformation describe-stacks --query "Stacks[?contains(Tags[], {Key: 'STAGE', Value: 'dev'})].[StackName,LastUpdatedTime]"
bash-5.1$ aws cloudformation describe-stacks | jq '[.Stacks[] | select(.Tags[] | contains({Key: "STAGE", Value: "dev"})) | [.StackName,.LastUpdatedTime]]'
[
    [
        "sls-page-tracker-dev",
        "2023-02-03T07:56:49.848Z"
    ],
    [
        "wwwstatuscheck-dev",
        "2022-12-20T11:07:21.155Z"
    ]
]
```

![More Complex](./images/ComplexStuff.jpg)

### Getting more complex

Let's do some sorting. Yes, they can do that, and have many other functions built in!

| Example          | AWS CLI query expression          | JQ Expression             |
|-|-|-|
| Sort output numerically by field values* | `sort_by(Items[*], &to_number(SomeField.N))[*][SortKey.S,SomeField.N]` | `[.Items[] | [.SortKey.S,.ServiceTime.N]] | sort_by(.[1] | tonumber)` |
| Sum fields (e.g. get total page access time ) | `sum(map(&to_number(ServiceTime.N), Items[*]))` | `[.Items[].ServiceTime.N | tonumber] | add`
| Perform counting e.g. sum of pages accessed by Mozilla | `length(Items[?AgentString && starts_with(AgentString.S, 'Mozilla')])` | `[.Items[] | select(.AgentString.S | startswith("Mozilla"))] | length`

\* _Note the expressions convert the fields to numbers here so as to sort numerically rather than textually_

In order to demonstrate one difference in capabilities, this is how you sort (ascending) the output of CloudFormation stacks by update date in JQ:

`aws cloudformation describe-stacks | jq '.Stacks | sort_by(.LastUpdatedTime | sub("\\.[0-9]*";"") | fromdate)'`

Now, you may say that the CLI JMES filter can do this as well, and you are technically correct, but that is because the ISO date is set up in a way that allows for text-based sorting. There may be instances where this type of sorting is not sufficient. There are also instances where data may be returned to you as a timestamp, but you wish to convert it to human-readable text, such as converting a list of timestamps into a readable dates.

_(The eagle-eyed amongst you will also note that you need to transform the update time with a regular expression substitution because the AWS date format does not confirm exactly to ISO8601)_

### Modifying JSON In-Place

The above examples are fine, but what about if you just want to modify data in-place, or even add to the JSON? In the example above what about if you wanted to transform the `cloudformation list-stacks` output so you get a count of all the stacks included with the results.

JMES only lets you do this by creating a new object:

`aws cloudformation list-stacks --query "{StackSummaries: StackSummaries, StackCount: length(@.StackSummaries)}"`

This is awkward because it seems you will need to re-create the original object fields. However it does offer the `merge` function:

`aws cloudformation list-stacks --query "merge(@, {StackCount: length(@.StackSummaries)})"`

JQ is more powerful in this regard, because it offers an assignment operator (unsurprisingly the `=` sign) which can also be suffixed to other operators. The JMES example becomes:

`jq '.StackCount = (.StackSummaries | length)'`

This can also be done with the `+` operator, which acts like the JMES `merge` function when given two objects:

`jq '. + {StackCount: .StackSummaries | length}'`

All of the above commands produce the following:

```
{
  "StackSummaries": [
    {
      "StackName": "my-website-stack",
      "CreationTime": "2019-09-24T04:21:45.435Z",
      "LastUpdatedTime": "2023-01-10T04:09:04.643Z",
      "StackStatus": "UPDATE_COMPLETE",
    },
    ...
  ],
  "StackCount": 6
}
```

But what about modifying fields in-place? Say we wanted to change the 'CreationTime' to a date without creating a new field? JMES cannot do this, partly because it is not good at modifying fields (or at least not easily), and also because the functions it offers are simple ones which don't modify the contents (like sum, min, abs, sort).

It's at this point that JQ starts pulling away from JMES. JQ is able to do this with the assignment operator, and its provided functions are more powerful. It does offer a REGEX feature, but for this simple example we can use the division operator `/`. This operator is a bit quirky: in a string context, the divide operator acts like the 'split' function. JQ does overload it's operators to do certain things in certain contexts.

```
bash-5.1$ aws cloudformation list-stacks | jq '.StackSummaries[].CreationTime |= (./ "T" | .[0])'
{
  "StackSummaries": [
    {
      "StackName": "my-website-stack",
      "CreationTime": "2019-09-24",
      "LastUpdatedTime": "2023-01-10T04:09:04.643Z",
      "StackStatus": "UPDATE_COMPLETE",
    },
    ...
  ]
}
```

To break this down:

  - `|=` is a pipe-and-assignment, so each `StackSummaries.CreationTime` is sent to the following expression and the result is assigned back.
  - `()` are needed because it contains an ambiguous expression
  - `./ "T"` takes the received input and divides it (splits it) on 'T'
  - `| .[0]` takes the output of the previous expression, which will be an array, and returns only the first element

This can be very powerful if the JSON you receive requires a few data transformations rather than restructuring.

![Customised](./images/customised.jpg)
### Handling 'custom' JSON

Nearly all the CLI's JSON output is in a form which can be easily queried by JMESPath filter expressions. AWS have probably done this for a reason. What I mean by this is that key names are descriptive of the data that it holds, such as `"Name"` and `"LastUpdatedDate"`, and information like tags appear in a list of `{"Key": "MyKey", "Value": "MyVal"}` objects, instead of `{"MyKey": "MyValue"}`.

In these cases, we perform filtering like seen above, using a filter expression like `[?Key=='MyKey']`. But what if the JSON data is structured the other way? An example of this is say a lambda which outputs a list of page visits where the key is the name of the page, like this:

```
{
  "blog/articles/2022-11-article/": 1071,
  "blog/articles/2021-11-favourite-article/": 1156,
  "blog/articles/2022-01-old-article/": 753,
  "blog/articles/2022-10-another-article/": 499,
  ...
}
```

In this case you can do two things - filter and sort on the actual key name, and sort on the value. Both of these things are achievable in `jq` thanks to built-in functions `to_entries`, `from_entries` and `with_entries`.

To filter on key names, we use `with_entries`. This function maps the given expression across each of the keys and values of the object, allowing you to access the key as `.key` and the value as `.value`. So to get all the articles with `2022` in the key, we do the following:

```
bash-5.1$ curl https://<my-api> | jq 'with_entries( select(.key | contains("2022")) )'
{
  "blog/articles/2022-11-article/": 771,
  "blog/articles/2022-01-old-article/": 1153,
  "blog/articles/2022-10-another-article/": 499,
  ...
}
```

We can further sort these keys by adding the `--sort-keys` argument to the `jq` command.

Before we go on to sorting by values, I will explain how `with_entries` is linked to `to_entries` and `from_entries`. `to_entries` is much like the Javascript function in that it converts an object into a list of `{'key': XXX, 'value': YYY}` objects. This is what allows you to use the `.key` and `.value` accessors in the example above. `from_entries` does the opposite, and `with_entries` is simply a shorthand for this. This means that the above example of filtering the key names using `with_entries` is exactly the same as the following:

```
bash-5.1$ curl https://<my-api> | jq 'to_entries | map(select(.key | contains("2022"))) | from_entries'
{
  "blog/articles/2022-11-article/": 771,
  "blog/articles/2022-01-old-article/": 1153,
  "blog/articles/2022-10-another-article/": 499,
  ...
}
```

Now that we understand this, we can sort our list by value:

```
bash-5.1$ curl https://<my-api> | jq 'to_entries | map(select(.key | contains("2022"))) | sort_by(.value) | reverse | from_entries'
{
  "blog/articles/2022-01-old-article/": 1153,
  "blog/articles/2022-11-article/": 771,
  "blog/articles/2022-10-another-article/": 499,
  ...
}
```

The key thing to notice here is we can't use `with_entries` with `sort_by`, because `sort_by` operates on a whole list; `with_entries` on the other hand applies the given function to each item which is why it works with filtering. Thus we execute the sort after the mapping of the `select` function has output a complete list.

The other small thing to notice is the need for `reverse`, because `sort_by` sorts in ascending order.

The JMES library used in the AWS CLI is not this powerful and cannot do this kind of filtering on key name or a value without a field context; it can filter the name but then there is no way to reference back to the original object. The AWS APIs have been designed so that the keys are not dynamic which does offer more flexibility in supporting more methods of querying the output, so for AWS CLI usage it should not be a problem.

## Wrapping Up

This post shows that it is possible to perform some complicated transformations on JSON output data, even to the point of creating new JSON data that another program can use. I think most people could see that the above commands, which you can almost call 1-liners, can replace a whole JavaScript or Python function and allow you to perform complicated ad-hoc and maybe even regular tasks, with much less development overhead.

In fact, because JQ can read your filter expression from a file (which can also contain comments), complex filters can turn into 1-liners, with JQ as your script interpreter. This also means that you can version-control and track your JQ scripts.

Overall I think these are very powerful techniques to know. While I touched above on the fact that with services like DynamoDB it is preferable to perform filtering on the server-side to avoid charges on your data access, it can still be useful for formatting and transforming output either for display purposes or to pass for use in other systems. For commands which return information on the services themselves, these two tools are still useful in decluttering output and presenting it nicely.

Finally, the specifications of these tools are quite similar and are available in library form in JavaScript, Python, Go and many other languages. Because of the limitations in parsing paths in the JMES specification, if your API outputs JSON it may be worth considering producing it in a way that allows it to be parsed and manipulated in the JMES fashion. This will allow it to be consumed more flexibly by tools and libraries.

![Red Pill Or Blue Pill](./images/redpillbluepill.jpg)

### Next step

Does this satisfy your current JSON processing needs? Or do you want more? What if I told you that you can write a data processing/ETL pipeline only using the JSON parsing tools shown above?

If you want to dive down this rabbit-hole then check out the [second part...](./2023-02-aws-cli-advanced-filtering-pt2.markdown)

### More Resources

[Filtering output from the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-filter.html)
