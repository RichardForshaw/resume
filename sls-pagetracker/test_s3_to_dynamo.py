# Test the handler functions
from pytest import mark
from handler import parse_log_string_to_dynamo, parse_s3_logs_to_dynamo, S3_LOG_TS_FORMAT

import re
from datetime import datetime

TEST_DATA_1 = '''
79a59df awsexamplebucket1 [06/Feb/2019:00:00:38 +0000] 192.0.2.3 - 3E57427F3EXAMPLE REST.GET.VERSIONING - "GET /awsexamplebucket1?versioning HTTP/1.1" 200 - 113 - 7 - "-" "S3Console/0.4" - s9lzHYrFp76ZVxRcpX9+5cjAnEH2ROuNkd2BHfIa6UkFVdtjf5mKR3/eTPFvsiP/XV/VLi31234= SigV2 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader awsexamplebucket1.s3.us-west-1.amazonaws.com TLSV1.1
79a59df awsexamplebucket1 [06/Feb/2019:00:00:38 +0000] 192.0.2.3 - 891CE47D2EXAMPLE REST.GET.LOGGING_STATUS - "GET /awsexamplebucket1?logging HTTP/1.1" 200 - 242 - 11 - "-" "S3Console/0.4" - 9vKBE6vMhrNiWHZmb2L0mXOcqPGzQOI5XLnCtZNPxev+Hf+7tpT6sxDwDty4LHBUOZJG96N1234= SigV2 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader awsexamplebucket1.s3.us-west-1.amazonaws.com TLSV1.1
79a59df awsexamplebucket1 [06/Feb/2019:00:00:38 +0000] 192.0.2.3 - A1206F460EXAMPLE REST.GET.BUCKETPOLICY - "GET /awsexamplebucket1?policy HTTP/1.1" 404 NoSuchBucketPolicy 297 - 38 - "-" "S3Console/0.4" - BNaBsXZQQDbssi6xMBdBU2sLt+Yf5kZDmeBUP35sFoKa3sLLeMC78iwEIWxs99CRUrbS4n11234= SigV2 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader awsexamplebucket1.s3.us-west-1.amazonaws.com TLSV1.1
79a59df awsexamplebucket1 [06/Feb/2019:00:01:57 +0000] 192.0.2.3 - DD6CC733AEXAMPLE REST.GET.OBJECT s3-dg.pdf "GET /awsexamplebucket1/folder/page-1.html HTTP/1.1" 200 - - 4406583 41754 28 "-" "S3Console/0.4" - 10S62Zv81kBW7BB6SX4XJ48o6kpcl6LPwEoizZQQxJd5qDSCTLX0TgS37kYUBKQW3+bPdrg1234= SigV4 ECDHE-RSA-AES128-SHA AuthHeader awsexamplebucket1.s3.us-west-1.amazonaws.com TLSV1.1
79a59df awsexamplebucket1 [06/Feb/2019:00:01:00 +0000] 192.0.2.3 - 7B4A0FABBEXAMPLE REST.GET.VERSIONING - "GET /awsexamplebucket1?versioning HTTP/1.1" 200 - 113 - 33 - "-" "S3Console/0.4" - Ke1bUcazaN1jWuUlPJaxF64cQVpUEhoZKEG/hmy/gijN/I1DeWqDfFvnpybfEseEME/u7ME1234= SigV2 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader awsexamplebucket1.s3.us-west-1.amazonaws.com TLSV1.1
79a59df awsexamplebucket1 [06/Feb/2019:00:01:57 +0000] 192.0.2.3 - DD6CC733AEXAMPLE REST.PUT.OBJECT s3-dg.pdf "PUT /awsexamplebucket1/s3-dg.pdf HTTP/1.1" 200 - - 4406583 41754 28 "-" "S3Console/0.4" - 10S62Zv81kBW7BB6SX4XJ48o6kpcl6LPwEoizZQQxJd5qDSCTLX0TgS37kYUBKQW3+bPdrg1234= SigV4 ECDHE-RSA-AES128-SHA AuthHeader awsexamplebucket1.s3.us-west-1.amazonaws.com TLSV1.1
79a59df awsexamplebucket1 [06/Feb/2019:00:01:00 +0000] 192.0.2.3 - 7B4A0FABBEXAMPLE REST.GET.VERSIONING - "GET /awsexamplebucket1?versioning HTTP/1.1" 200 - 113 - 33 - "-" "S3Console/0.4" - Ke1bUcazaN1jWuUlPJaxF64cQVpUEhoZKEG/hmy/gijN/I1DeWqDfFvnpybfEseEME/u7ME1234= SigV2 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader awsexamplebucket1.s3.us-west-1.amazonaws.com TLSV1.1
79a59df awsexamplebucket1 [06/Feb/2019:00:01:57 +0000] 192.0.2.3 - DD6CC733AEXAMPLE REST.GET.OBJECT s3-dg.pdf "GET /awsexamplebucket1/s3-dg.pdf HTTP/1.1" 200 - - 4406583 41754 28 "-" "S3Console/0.4" - 10S62Zv81kBW7BB6SX4XJ48o6kpcl6LPwEoizZQQxJd5qDSCTLX0TgS37kYUBKQW3+bPdrg1234= SigV4 ECDHE-RSA-AES128-SHA AuthHeader awsexamplebucket1.s3.us-west-1.amazonaws.com TLSV1.1
'''.splitlines()

TEST_DATA_2 = '''
d6ad5f7 www.forshaw.tech [06/Sep/2022:06:41:03 +0000] 14.161.28.234 - XT82V8BT213DR64T WEBSITE.GET.OBJECT favicon.ico "GET /favicon.ico HTTP/1.1" 404 NoSuchKey 346 - 13 - "http://www.forshaw.tech/blog/articles/2022-08-30-aws-cli-essentials/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0" - LGH74mdQgyY07NqnWC0ugVllKEtmmK/BvK+ik/4FhFFyYLmsUwsZWfGLEkVxd02+5IRecuQVjOk= - - - www.forshaw.tech - -
d6ad5f7 www.forshaw.tech [06/Sep/2022:06:41:03 +0000] 14.161.28.234 - XT85DJ4DWDWEXF24 WEBSITE.GET.OBJECT blog/search/worker.js "GET /blog/search/worker.js HTTP/1.1" 200 - 3724 3724 56 56 "http://www.forshaw.tech/blog/articles/2022-08-30-aws-cli-essentials/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0" - eFOhAIqQCvqDYy62f4ZLKSF/5sQJR1vEsz0yGTTPiM1GUia9zPxbNe5iEKqroJntChBe6D/7Ybc= - - - www.forshaw.tech - -
d6ad5f7 www.forshaw.tech [06/Sep/2022:06:40:21 +0000] 14.161.28.234 - RAF3CVEDSB2XCEKJ REST.GET.VERSIONING - "GET /www.forshaw.tech?versioning= HTTP/1.1" 200 - 113 - 26 - "-" "S3Console/0.4, aws-internal/3 aws-sdk-java/1.11.1030 Linux/5.4.207-126.363.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.302-b08 java/1.8.0_302 vendor/Oracle_Corporation cfg/retry-mode/standard" - frNwIwOjTi8e2zxsZBTNyf2RTM8wiD5V3NVatZpdKodqFlmOopQImBev4gBIgHfZLHWa6PmjY5w= SigV4 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader s3.ap-southeast-1.amazonaws.com TLSv1.2 -
d6ad5f7 www.forshaw.tech [06/Sep/2022:06:40:21 +0000] 14.161.28.234 - RAFDP3EM1ZPY1A58 REST.GET.OWNERSHIP_CONTROLS - "GET /www.forshaw.tech?ownershipControls= HTTP/1.1" 404 OwnershipControlsNotFoundError 294 - 30 29 "-" "S3Console/0.4, aws-internal/3 aws-sdk-java/1.11.1030 Linux/5.4.207-126.363.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.302-b08 java/1.8.0_302 vendor/Oracle_Corporation cfg/retry-mode/standard" - FnCeUrfIC7Rrg51ZvRieLQysRE98D/V6GB7hIY/AeIc5hm9NAU+wwrCB1M81oVXd7YHgD5AUIOc= SigV4 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader s3.ap-southeast-1.amazonaws.com TLSv1.2 -
d6ad5f7 www.forshaw.tech [06/Sep/2022:06:40:24 +0000] 14.161.28.234 - BP8Y4YFRSJWSAK4G REST.GET.ACCELERATE - "GET /www.forshaw.tech?accelerate= HTTP/1.1" 200 - 113 - 10 - "-" "S3Console/0.4, aws-internal/3 aws-sdk-java/1.11.1030 Linux/5.4.207-126.363.amzn2int.x86_64 OpenJDK_64-Bit_Server_VM/25.302-b08 java/1.8.0_302 vendor/Oracle_Corporation cfg/retry-mode/standard" - Dolf8oNcfkmhVbySSTZs/y2CoOqTB0tNQGBwGVFNaHc+DjgTckp42rueVDJjG2/IvRQBJ5ZgO34= SigV4 ECDHE-RSA-AES128-GCM-SHA256 AuthHeader s3.ap-southeast-1.amazonaws.com TLSv1.2 -
d6ad5f7 www.forshaw.tech [06/Sep/2022:06:41:03 +0000] 14.161.28.234 - XT8A9NN2MFQ6B2AY WEBSITE.GET.OBJECT blog/search/search_index.json "GET /blog/search/search_index.json HTTP/1.1" 200 - 207989 207989 61 59 "http://www.forshaw.tech/blog/search/worker.js" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0" - wNy5q7GnuPrqocIniVVHQHIB9KBpZXsuaBPbCXKET8Oe1+b21p1018ehEek4I7NjBnu+BeB8yik= - - - www.forshaw.tech - -
d6ad5f7 www.forshaw.tech [06/Sep/2022:06:41:06 +0000] 14.161.28.234 - PPQ0R24HD4WYJ420 WEBSITE.GET.OBJECT blog/index.html "GET /blog/ HTTP/1.1" 200 - 16630 16630 40 40 "http://www.forshaw.tech/blog/articles/2022-08-30-aws-cli-essentials/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0" - 6KIcjW6RV2ooqmSw6k5DZAwdO7Cc8tpWIMd0kqXVrArEyReHi6n6iPve9CywbS4M/eeBd8n7rro= - - - www.forshaw.tech - -
d6ad5f7 www.forshaw.tech [06/Sep/2022:06:41:06 +0000] 14.161.28.234 - PPQ6CFA6K97KP375 WEBSITE.GET.OBJECT blog/StaticWebSiteDevOps_Basic.png "GET /blog/StaticWebSiteDevOps_Basic.png HTTP/1.1" 200 - 50767 50767 47 46 "http://www.forshaw.tech/blog/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0" - 9Xn54PiT2XckZARdUb3cOe02qUHgr9RWPFmQroPC1WZ8WgJD6v1q37+F2QjK8d7JMAtr6dtwlR8= - - - www.forshaw.tech - -
d6ad5f7 www.forshaw.tech [06/Sep/2022:06:41:02 +0000] 14.161.28.234 - 1ZV2ZPXST2EY8SKQ WEBSITE.GET.OBJECT blog/articles/2022-08-30-aws-cli-essentials/index.html "GET /blog/articles/2022-08-30-aws-cli-essentials/ HTTP/1.1" 200 - 30224 30224 89 87 "http://www.forshaw.tech/blog/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0" - Gl7Ntr8mZByYxg8QKlM8pSrrNErIsoWFUDgfBcuLve1Odt4tavzOI7BCtmT3PggCeIHYlOybN4E= - - - www.forshaw.tech - -
'''.splitlines()

TEST_DATA_3 = '''
d6ad5f7 www.forshaw.tech [06/Sep/2022:07:13:09 +0000] 14.161.28.234 - R0VXAK9B994MMD0Y WEBSITE.GET.OBJECT blog/StaticWebSiteDevOps_Basic.png "GET /blog/StaticWebSiteDevOps_Basic.png HTTP/1.1" 200 - 50767 50767 65 64 "http://www.forshaw.tech/blog/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0" - XwOXLzeYshuzdNgxVO0ylp9SPJcMCzlYJyoUav/7tldi/RmebX29JsmDTeRoqCb3Be+ysc+Rgsc= - - - www.forshaw.tech - -
d6ad5f7 www.forshaw.tech [06/Sep/2022:07:13:09 +0000] 14.161.28.234 - R0VXNJ04EPPXYSYY WEBSITE.GET.OBJECT blog/index.html "GET /blog/ HTTP/1.1" 200 - 16630 16630 88 87 "http://www.forshaw.tech/blog/articles/2022-08-24-first-vietnam-experiences/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0" - dpVWRUdeno1JPQs2h2amMsLbRDHzRcR4+oQbZcU6frg/tbdACOcZbW0NXW8iSiYN8oMAU+xfmG0= - - - www.forshaw.tech - -
d6ad5f7 www.forshaw.tech [06/Sep/2022:07:13:17 +0000] 14.161.28.234 - 90TMWQWF2WPNHAXP WEBSITE.GET.OBJECT blog/articles/images/calculator.jpg "GET /blog/articles/images/calculator.jpg HTTP/1.1" 200 - 341523 341523 82 79 "http://www.forshaw.tech/blog/articles/2018-11-28-backlog-priorities/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0" - gUgfcMlF5DOzWW/Q9r1rHIjltNqiCcoCCYiiaKk/R5T6uigSHwz5Ts6Zw3vqclYVWAMteDQT0wM= - - - www.forshaw.tech - -
d6ad5f7 www.forshaw.tech [06/Sep/2022:07:13:17 +0000] 14.161.28.234 - 90TZPQQ22YE0AK0X WEBSITE.GET.OBJECT blog/articles/2018-11-28-backlog-priorities/index.html "GET /blog/articles/2018-11-28-backlog-priorities/ HTTP/1.1" 200 - 17683 17683 67 66 "http://www.forshaw.tech/blog/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0" - P17UhZ9xnGTr3ZLNh6x6uauvM9EcWUJ9ujfDLdtvm+5nKUMg9x7DoHanhClejMkb0rsG+pHNAO4= - - - www.forshaw.tech - -
'''

@mark.parametrize('test_data,field_tuples,expected',
    [
        (TEST_DATA_1[1], ((1, 'BucketName', 'S'),), { 'BucketName': {'S': 'awsexamplebucket1'} }),
        (TEST_DATA_1[4], ((3, 'RemoteAddress', 'S'),), { 'RemoteAddress': {'S': '192.0.2.3'} }),
        (TEST_DATA_1[3], ((9, 'HTTPResult', 'N'),), { 'HTTPResult': {'N': 404} }),
        (TEST_DATA_2[1], ((1, 'BucketName', 'S'),), { 'BucketName': {'S': 'www.forshaw.tech'} }),
        (TEST_DATA_2[6], ((13, 'ThirdNumber', 'N'),), { 'ThirdNumber': {'N': 61} }),
        (TEST_DATA_2[9], ((7, 'PageName', 'S'),), { 'PageName': {'S': 'blog/articles/2022-08-30-aws-cli-essentials/index.html'} }),
    ])
def test_parse_single_log_string_field_to_dynamo_dict(test_data, field_tuples, expected):

    result = parse_log_string_to_dynamo(test_data, field_tuples)
    assert result == expected

@mark.parametrize('test_data,field_tuples,format,expected',
    [
        (TEST_DATA_1[1], ((1, 'BucketName', 'S'),), 'Test#{}', { 'BucketName': {'S': 'Test#awsexamplebucket1'} }),
        (TEST_DATA_1[4], ((3, 'RemoteAddress', 'S'),), 'Address#{}#Key', { 'RemoteAddress': {'S': 'Address#192.0.2.3#Key'} }),
        (TEST_DATA_2[1], ((1, 'PK', 'S'),), 'Weird--{}--Format', { 'PK': {'S': 'Weird--www.forshaw.tech--Format'} }),
    ])
def test_parse_log_string_with_pk_format_rule(test_data, field_tuples, format, expected):

    result = parse_log_string_to_dynamo(test_data, field_tuples, pk_format=format)
    assert result == expected

@mark.parametrize('test_data,field_tuples,trans_fn,expected',
    [
        (TEST_DATA_1[1], ((1, 'BucketName', 'S'),), {'BucketName': str.upper}, { 'BucketName': {'S': 'AWSEXAMPLEBUCKET1'} }),
        (TEST_DATA_1[4], ((3, 'RemoteAddress', 'S'),), {'RemoteAddress': lambda x: x.split('.')}, { 'RemoteAddress': {'S': ['192', '0', '2', '3']} }),
        (TEST_DATA_2[4], ((2, 'Timestamp', 'N'),), {'Timestamp': lambda x: int(datetime.strptime(x, S3_LOG_TS_FORMAT).timestamp())}, { 'Timestamp': {'N': 1662446421} }),
    ])
def test_parse_log_string_with_field_translation_rule(test_data, field_tuples, trans_fn, expected):

    result = parse_log_string_to_dynamo(test_data, field_tuples, translations=trans_fn)
    assert result == expected

@mark.parametrize('test_data,field_tuples,format,expected',
    [
        (TEST_DATA_1[1], ((1, 'BucketName', 'S'), (3, 'RemoteAddress', 'S'), (9, 'HTTPResult', 'N')), 'Test#{}',
            { 'BucketName': {'S': 'Test#awsexamplebucket1'}, 'RemoteAddress': { 'S': '192.0.2.3'}, 'HTTPResult': {'N': 200 } }),
        (TEST_DATA_2[7], ((7, 'PK', 'S'), (1, 'BucketName', 'S'), (13, 'ServiceTime', 'N')), 'Richard#{}',
            { 'PK': {'S': 'Richard#blog/index.html'},  'BucketName': {'S': 'www.forshaw.tech'}, 'ServiceTime': { 'N': 40 } }),
    ])
def test_parse_multi_log_string_fields_to_dynamo_dict(test_data, field_tuples, format, expected):

    result = parse_log_string_to_dynamo(test_data, field_tuples, pk_format=format)
    assert result == expected

def test_parse_and_format_and_translate_pk():
    field_tuples = ((1, 'BucketName', 'S'),)
    trans_fn = {'BucketName': str.upper }
    pk_format = 'Formatted-{}'

    result = parse_log_string_to_dynamo(TEST_DATA_1[1], field_tuples, translations=trans_fn, pk_format=pk_format)
    assert result == { 'BucketName': { 'S': 'Formatted-AWSEXAMPLEBUCKET1'}}

def test_parse_log_string_array_to_dynamo_dict_list():

    field_tuples = ((7, 'UserPages', 'S'), (2, 'SortKey', 'S'), (16, 'AgentString', 'S'), (13, 'ServiceTime', 'N'))
    result = parse_s3_logs_to_dynamo(TEST_DATA_2[:7],
                    field_tuples,
                    pk_format="Richard#{}",
                    translations={"SortKey": lambda x: str(int(datetime.strptime(x, S3_LOG_TS_FORMAT).timestamp()))})

    assert result == [
        {
            'UserPages': { 'S': 'Richard#favicon.ico'},
            'SortKey': { 'S': '1662446463'},
            'AgentString': { 'S': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'},
            'ServiceTime': { 'N': 13}
        },
        {
            'UserPages': { 'S': 'Richard#blog/search/worker.js'},
            'SortKey': { 'S': '1662446463'},
            'AgentString': { 'S': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'},
            'ServiceTime': { 'N': 56}
        },
        {
            'UserPages': { 'S': 'Richard#blog/search/search_index.json'},
            'SortKey': { 'S': '1662446463'},
            'AgentString': { 'S': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'},
            'ServiceTime': { 'N': 61}
        }
    ]

def test_parse_empty_string():
    assert parse_s3_logs_to_dynamo('', ((7, 'UserPages', 'S'), (2, 'SortKey', 'S'))) == []

def test_parse_multi_line_string_to_dynamo_dict_list():

    field_tuples = ((7, 'UserPages', 'S'), (2, 'SortKey', 'S'), (13, 'ServiceTime', 'N'))
    result = parse_s3_logs_to_dynamo(TEST_DATA_3,
                    field_tuples,
                    pk_format="Richard#{}",
                    translations={"SortKey": lambda x: str(int(datetime.strptime(x, S3_LOG_TS_FORMAT).timestamp()))})

    assert result == [
        {
            'UserPages': { 'S': 'Richard#blog/StaticWebSiteDevOps_Basic.png'},
            'SortKey': { 'S': '1662448389'},
            'ServiceTime': { 'N': 65}
        },
        {
            'UserPages': { 'S': 'Richard#blog/index.html'},
            'SortKey': { 'S': '1662448389'},
            'ServiceTime': { 'N': 88}
        },
        {
            'UserPages': { 'S': 'Richard#blog/articles/images/calculator.jpg'},
            'SortKey': { 'S': '1662448397'},
            'ServiceTime': { 'N': 82}
        },
        {
            'UserPages': { 'S': 'Richard#blog/articles/2018-11-28-backlog-priorities/index.html'},
            'SortKey': { 'S': '1662448397'},
            'ServiceTime': { 'N': 67}
        }
    ]


def test_parse_log_entries_views_with_bucket_filter():

    field_tuples = ((7, 'UserPages', 'S'), (1, 'BucketName', 'S'))
    result = parse_s3_logs_to_dynamo(TEST_DATA_1 + TEST_DATA_3.splitlines(),
                    field_tuples,
                    bucket_name='www.forshaw.tech',
                    pk_format="Format#{}")

    assert result == [
        {
            'UserPages': { 'S': 'Format#blog/StaticWebSiteDevOps_Basic.png'},
            'BucketName': { 'S': 'www.forshaw.tech'}
        },
        {
            'UserPages': { 'S': 'Format#blog/index.html'},
            'BucketName': { 'S': 'www.forshaw.tech'}
        },
        {
            'UserPages': { 'S': 'Format#blog/articles/images/calculator.jpg'},
            'BucketName': { 'S': 'www.forshaw.tech'}
        },
        {
            'UserPages': { 'S': 'Format#blog/articles/2018-11-28-backlog-priorities/index.html'},
            'BucketName': { 'S': 'www.forshaw.tech'}
        }
    ]

    field_tuples = ((7, 'UserPages', 'S'), (1, 'BucketName', 'S'))
    result = parse_s3_logs_to_dynamo(TEST_DATA_1 + TEST_DATA_3.splitlines(),
                    field_tuples,
                    bucket_name='awsexamplebucket1',
                    pk_format="Format#{}")

    assert result == [
        {
            'UserPages': { 'S': 'Format#s3-dg.pdf'},
            'BucketName': { 'S': 'awsexamplebucket1'}
        },
        {
            'UserPages': { 'S': 'Format#s3-dg.pdf'},
            'BucketName': { 'S': 'awsexamplebucket1'}
        }
    ]

def test_parse_log_entries_views_with_folder_filter():
    field_tuples = ((7, 'UserPages', 'S'), (1, 'BucketName', 'S'))
    result = parse_s3_logs_to_dynamo(TEST_DATA_3,
                    field_tuples,
                    bucket_name='www.forshaw.tech',
                    folder_prefix='blog/articles',
                    pk_format="Format#{}")

    assert result == [
        {
            'UserPages': { 'S': 'Format#blog/articles/images/calculator.jpg'},
            'BucketName': { 'S': 'www.forshaw.tech'}
        },
        {
            'UserPages': { 'S': 'Format#blog/articles/2018-11-28-backlog-priorities/index.html'},
            'BucketName': { 'S': 'www.forshaw.tech'}
        }
    ]

# TODO: ONLY MATCH index.html AND strip out index.html from result...

def test_parse_log_entries_with_file_filter():
    field_tuples = ((7, 'UserPages', 'S'), (1, 'BucketName', 'S'))
    result = parse_s3_logs_to_dynamo(TEST_DATA_3,
                    field_tuples,
                    bucket_name='www.forshaw.tech',
                    file_filter='index.html')

    assert result == [
        {
            'UserPages': { 'S': 'blog/index.html'},
            'BucketName': { 'S': 'www.forshaw.tech'}
        },
        {
            'UserPages': { 'S': 'blog/articles/2018-11-28-backlog-priorities/index.html'},
            'BucketName': { 'S': 'www.forshaw.tech'}
        }
    ]

def test_parse_with_file_filter_and_strip_file_name():
    field_tuples = ((7, 'UserPages', 'S'), (1, 'BucketName', 'S'))
    result = parse_s3_logs_to_dynamo(TEST_DATA_3,
                    field_tuples,
                    bucket_name='www.forshaw.tech',
                    file_filter='index.html',
                    translations={"UserPages": lambda x: re.sub(r'index\.html', '', x)})

    assert result == [
        {
            'UserPages': { 'S': 'blog/'},
            'BucketName': { 'S': 'www.forshaw.tech'}
        },
        {
            'UserPages': { 'S': 'blog/articles/2018-11-28-backlog-priorities/'},
            'BucketName': { 'S': 'www.forshaw.tech'}
        }
    ]

