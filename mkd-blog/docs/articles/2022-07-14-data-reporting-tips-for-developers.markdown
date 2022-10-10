---
layout: post
title:  "Data Reporting Tips For Developers"
description: "If you are a developer and are working for a growing small tech business, chances are you may have to assist with some data reporting with a database or BI tool. In here I discuss some tips to help develop exactly the reports that they need."
date: "2022-07-14"
revision_date: "2022-07-14"
tags:
    - Reporting and BI
    - Databases
author: Richard Forshaw
---

![report graphics](images/data-visualization-tools.jpg "Date Reporting Graphics")

If you are a developer and are working for a growing small tech business, chances are you may have to assist with some data reporting. All businesses need this, and the best thing to do to help the business owners is to help develop exactly the reports that they need. This data may include analysis on revenue, profit, most valuable customers, most profitable business categories or most and least used app functions.

## Tooling

It is possible that you can (or have already) bake these reports straight into your software, however this often comes with a high level of overhead, which may include:

 - searching for and selecting a data visualisation package
 - provisioning read-only follower databases with additional analysis fields
 - lover level knowledge and storage of database queries
 - ensuring installed packages and libraries supporting your visualisations are up to date
 - handling interface or behaviour changes to the same packages

all of which, while giving you ultimate control, will add to your delivery time and may introduce impromptu unwanted delays later on.

The alternative is to use a BI tool. These also come in a wide range of flavours with differing prices, complexity and capabilities. However they should drastically cut the implementation overheads, albeit with the trade-off of some loss of control and having to pay some fees. But in many instances, especially for small businesses with basic or intermediate reporting requirements, these BI tools will do the trick.

We used to use ChartIO for reporting, which was an excellent tool, mainly because it had a mature data-modeling tool which allowed non-technical people to generate the queries that they needed. We found that maybe only 10-15% of queries actually needed any technical assistance, and most of that was up-front and one-time only.

Unfortunately ChartIO was closed down this year after being bought by Atlassian. So after a brief search for other products matching our scope and budget, we selected [Bipp.io](http://bipp.io). We found out that Bipp was a little immature compared to our experience with ChartIO, which mainly meant that we needed some more technical input to get the reports we needed. However, they are pumping out regular updates, and it did mean that it gave me cause to write this article! (In fact while writing this they have already improved their platform.)

## Basic Setup

It is likely that whatever BI tool you use, you will need to set up a data source and model, the data source being the connection to your database and the model being a description of the data that you have.

The data source is straightforward to set up in most BI tools and usually requires access to your DB URL, however there are 2 tips I recommend doing. Either:

 - Create a new follower database from your master OR
 - at least create a new set of user credentials which are READ ONLY (and may resrict access to some sensitive tables)

This is of course to ensure that no accidents happen! Setting up a separate user is usually simpler and cheaper, but having a follower database is usually more flexible, especially if there are many people wanting to do different type of analysis since it will allow you to  implement your own 'view' of the data which is tailored to business analysis use (this is useful but beyind the scope of this article).

## Data Model

The Data Model is where you describe to the BI tool what your data looks like and perform any additional modeling on the raw database data. Usually the tool will be able to detect what your basic metadata is (i.e. column name, data type etc). However as with the case of Bipp, this is also where you need to:

 - Convert abbreviations into English names (e.g. your database format may use codes or single-letter abbreviations which are not very useful in reporting)
 - Provide formatting conventions (e.g. adding currency symbols to your chosen payment data formatting)
 - Define 'buckets' to later use for grouping and filtering (descibed later in this article)
 - prove some data 'decoration' to make it more relevant to your business users (e.g. you may want to break pricing down into price components or cost centers, or label transactions by quarter)
 - Perform any necessary table joining

 The joining item is an odd one - ChartIO allowed the analyst to join at the point the query was written, however Bipp requires that you perform the joining at the modeling stage*. So YMMV depending on your BI tool of choice.

 (* Since writing this, Bipp has provided a query feature which means you don't have to join tables in advance)

## Reports

Reports are where the fun stuff happens, and you get to turn mundane data queries into beautiful and meaningful graphics, if you do it right! Here are some gotchas that I had to solve, and you may need to as well.

### Dates

![a calendar](images/Calendar_thin.jpg "Dealing with Dates")

Everyone agrees that dates are fun (time zones and daylight savings anyone?). But they are made even more fun when you need to query them in reports. Bipp makes it easy to look at current day, week, quarter and year as they have a built-in magic drop-down selector which seems to do some dynamic text substitution, but what if you want to select other date ranges? This case may not always be supported by the built-in querying tool, and so you may need to write your own SQL filter.

We use Postgres, and the following functions became my friends: `'date_trunc'`, and `'interval'`.

Want to select data for the previous completed week? Select where:
```
(your_date_record > date_trunc('week', CURRENT_DATE - interval '1 week')) AND (your_date_record < date_trunc('week', CURRENT_DATE ))
```
(Note I have omitted any time zone conversions for clarity... I trust you are storing your dates in a standard ISO format!)

Want to select data for the last completed month?
```
(your_date_record > date_trunc('month', CURRENT_DATE - interval '1 month')) AND (your_date_record < date_trunc('month', CURRENT_DATE ))
```
or as a shorter alternative:
```
TO_CHAR(your_date_record, 'YYYYMM') == TO_CHAR((CURRENT_DATE - interval '1 month'), 'YYYYMM')
```

The second item formats the year and month as a character string and then compares it. This is also one way of filtering dates (see next section).

### Comparing time periods

Your business will undoubtedly want to compare how it is improving, for example from last month to this month. We have seen above how to select records which include both this month and last month, but how to display these comparatively?

One way of doing this is to perform a transformation on your date column so that you are able to group related information. A simple example is to transform your appropriate date column into a 'Year-month' label, so that you can group on the same month period. As of writing there was not an obvious way of doing this in Bipp, so it was required to be done in the data model, and other platforms may be similar. However in the final query it looks like this:
```
SELECT
  TO_CHAR(your_date_record, 'YYYYMM') AS date_bucket, Count(*) AS ItemCount, SUM(some_accumlating_value) AS AccumValue
  FROM ([your select query]) AS T
  WHERE date(T.your_date_record) >= date_trunc('month', CURRENT_DATE - interval '1 month')
GROUP BY date_bucket ORDER BY date_bucket
```

[Note that here `your_date_record` must be a valid date type. Comparing a date and timestamp may not give the correct result. This post does not dictate how you store your timestamps, except to recommend that you store them with timezone info.]

This will essentially use your_date_record to 'label' the record as something that is group-able (in this case `date_bucket`), apply a filter (that we learned about above) and then group (and sort) by your labels. Hey presto, you can render this as a table or a bar chart and see how your month so far compares to your previous month.

The same can be done for year and week, and even quarters (thank to the `Q` formatter).

### When weeks are different

The fun starts when you want to break things down by week. Doing a daily query or monthly query is straightforward and behaves as you would expect. Weeks however require a little extra knowledge.

Weeks come in two flavours - the standard Monday-Sunday week that humans operate on (or perhaps Sunday-Saturday depending on where you are from), and the _ordinal week of the year_. This ordinal week of the year presents problems, as your database date manipulation function of choice may use this flavour without you really knowing about it.

Your first thought may be to modify the query above which filtered on this month's and last month's data and simply change the grouping to group by week number and change the filter to use weeks instead of months. But this is where it goes wrong.

Referencing a 'week' in `TO_CHAR` may or may not return a week number in what is known as the [ISO week-numbering system](https://en.wikipedia.org/wiki/ISO_week_date). The basic difference is that the ISO week number starts on a Monday, whereas the regular 'week of the year' starts on the 1st of January. You can see that in 6 years out of 7 these will be different. The key takeaway is:

 - `TO_CHAR` with `WW` will return the week number where the 1st week starts on 1st Jan
 - `TO_CHAR` with `IW` will return the ISO week number which starts on a Monday
 - `EXTRACT` and `date_trunc` also work on ISO weeks which start on Monday
 - Stick to ISO weeks in most cases

So to get the previous week's date, filter on:
```
WHERE your_date_record > date_trunc('week', CURRENT_DATE - interval '1 week') AND your_date_record < date_trunc('week', CURRENT_DATE)
```

If however you try to re-use and modify the 'monthly' query seen previously using `TO_CHAR`:
```
WHERE TO_CHAR(your_date_record, 'YYYYWW') >= TO_CHAR((CURRENT_DATE - interval '1 week'), 'YYYYWW')
```
you are likely to confuse people and it will not match up with other queries, because this results in week-numbering beginning on 1st Jan. However you can use `IYYYIW` instead of `YYYYWW`, but I think the previous example is clearer.

### Non-standard time intervals

What happens if you want to do something a bit more exotic? Your country, as like many countries, may have a financial year which does not run Jan-Dec. So how do you specify buckets which delineate on a non-standard date?

In the latest major version of Postgres (as of writing), there is a `date_bin` function which allows dates to be easily identified in 'bins' (a common statistical tool), however since we don't have that version of Postgres yet (and I suspect some readers also don't), I present a solution which also works, although it is a bit longer.

Given that the financial year that we require runs between July and June, we can simply adjust the date in question by 6 months, truncate the year and then convert it into a text string. Countries with different financial year requirements will simply need a different adjustment.

```
CONCAT(TO_CHAR(date_trunc('year', "created" - interval '6 months'), '"FY"YY-'), TO_CHAR(date_trunc('year', "created" + interval '6 months'), 'YY')) as FinYear
```

This creates a column of the format "FYxx-yy" which can then be used for filtering or grouping.

### Playing around

Head on over to [DBFiddle](https://www.db-fiddle.com/). There you can pick your database type and play around with date functions. You will need to set up a table first, but that is as easy as:
```
CREATE TABLE t(id int)
```

Now you can try out many of the functions above to see what happens. You don't need any data in the table to use the functions described above, you just have to insert some valid date strings (or the built-in `CURRENT_DATE` where you need them to see the results.

