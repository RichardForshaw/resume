---
layout: post
title:  "ChatTDD: Pair Programming with AI"
description: "So ChatGPT can help in capturing product requirements, which is part of the way to generating a working product. But what about the next step? Can an AI help turn your ideas into code?"
tags:
    - Programming Techniques
    - AI
author: Richard Forshaw
---

In the last post, I wrote about the first stage of transforming an idea into working code using ChatGPT as an assistant. I took an idea and put ChatGPT through a BDD process and an Example Mapping process.

I was very impressed with the results, but also a bit disappointed from its lack of detail and also lack of determinism. It was not enough to rely on, but I do think it made a useful tool to simply speed this process up.

What about the second step - transforming an example scenario into code?

![Laptop and requirements](./images/aitdd/laptop_and_papers.jpg)

## Picking up from Requirements

In the last post, ChatGPT helped with creating BDD-type scenarios for a simple email parser. Now we will try to convert some of those scenarios into tests and code, using a typical TDD process. We will use one failure case and one success case. The cases are not exactly how ChatGPT gave them to us because as we learnt it was not very good at going down to the detail level. So in between that step and this step there needs to be some manual review and refinement of the cases.

The failure case:

``` properties
Scenario: Email with no file attachments returns error
  Given an email with no image file attachments
  When the email is sent to 'The System'
  Then the system should return an error code with the message "One image file attachment must be present."
```

The success case is essentially a text-processing requirement:

``` properties
Scenario: Email describing a single post item saves outputs correctly
  Given an email with the subject "INSTAGRAM POST 2023-04-01"
  And the email has body text
    """
    --- POST TEXT
    This is the post text
    --- CAPTION
    This is the caption
    ---
    """
  And the email has a single JPG attachment named
  When the email is sent to 'The System'
  Then the system should save the attachment as "POST-2023-04-01-01.JPG"
  And the system should save a file named "POST-2023-04-01.json"
  And the json file should have the contents:
    """
    {
        post_text: "This is the post text",
        captions: [
            {
                caption_text: "This is the caption",
            },
        ]
    }
    """
```

This is a fairly complex case, but it is specific. We will see how it works out.

## Setup

### Configure ChatGPT

To turn ChatGPT into a developer, I gave it the following system command:

``` txt
You are an expert python software developer. You know how to understand BDD scenarios of the form:

Scenario: scenario title
Given (an initial context)
When (an event occurs)
Then (a testable outcome is satisfied)

You know TDD and how to write tests first using pytest and pytest-bdd. When writing code, you favour functional programming and avoid side-effects.

You have been asked to assist another python software developer to develop tests and code for a small library to parse email content according to the given BDD specifications.
```

## Test 1: Simple failure case

### Writing the test case

I prompted ChatGPT with this prompt:

``` txt
Given the following scenario:

<scenario from above>

Write a pytest-bdd test which satisfies this scenario.
```

and I received the following code:

``` py
import pytest
from email_parser import parse_email

@pytest.mark.parametrize("email_content, expected_output", [
    ("Hello World", "One image file attachment must be present."),
    ("", "One image file attachment must be present."),
    ("image.jpg", "One image file attachment must be present."),
])
def test_parse_email_no_file_attachments(email_content, expected_output):
    # Given an email with no image file attachments
    email = {
        "content": email_content,
        "attachments": []
    }

    # When the email is sent to 'The System'
    output = parse_email(email)

    # Then the system should return an error code with the message "One image file attachment must be present."
    assert output == (False, expected_output)
```

Not quite the start I was expecting. Some things to note:

 1. It assumed a name for the module and for the function under test, which is fine. We will see if it remembers this
 2. It assumed an input format to the function under test as a single json structure
 3. It assumed an output from the function under test as a tuple.
 4. It has not used the pytest-bdd library as we requested in the system message
 5. The parameterization of the test is not really necessary. The test really only needs one example of having no attachments.

The second item is interesting, and I like it. The design that initially came into my head was that the function in question would parse the entire email message and handle the extraction of body text and attachments. When I initially saw the output from ChatGPT I was annoyed but then it made me think: this is actually a better solution. Perhaps it was even following my direction to program in a functional way?

I like writing things in a functional way. Typically it is good to write simple functions that do only one thing with no side-effects, which means they are easier to tests. In the long run I probably would have refactored the code to do this, but the ChatGPT output made me take this decision earlier, and I changed the design in my head to first parse the email into its sub-parts and then process the parts according to my requirements.

To fix the other issues, I instructed ChatGPT to refine the solution, by asking it to:

 * use the pytest-bdd library format, providing it with a scenario file name
 * return a json structure instead of a tuple

The updated test function was this:

``` py
import pytest
from pytest_bdd import given, when, then, scenario
from email_parser import parse_email

@scenario('../features/email-parsing.feature', 'Email with no file attachments returns error')
def test_parse_email_no_file_attachments():
    pass

@given("an email with no image file attachments")
def email_with_no_file_attachments():
    email = {
        "content": "Hello World",
        "attachments": []
    }
    return email

@when("the email is sent to 'The System'")
def send_email_to_system(email_with_no_file_attachments):
    return parse_email(**email_with_no_file_attachments)

@then("the system should return an error code with the message \"One image file attachment must be present.\"")
def check_error_message(send_email_to_system):
    expected_output = {
        "success": False,
        "error_message": "One image file attachment must be present."
    }
    assert send_email_to_system == expected_output
```

That looks like a pretty good bdd-style test to me.

### Implementing Code

When I ran the code, I got the usual errors, as you would expect from real TDD:

 * No module
 * No function
 * No scenario file

I fixed these up and then asked ChatGPT to write the code.

![Writing code](./images/aitdd/code.jpg)

``` txt
Now write the code which satisfies the test function.
```

The response was this (line-splitting done by me):

``` py
def parse_email(content, attachments):
    # Check if there are any image file attachments
    has_image_attachment = False
    for attachment in attachments:
        if attachment.get("name", "").lower().endswith(".jpg") \
            or attachment.get("name", "").lower().endswith(".jpeg") \
            or attachment.get("name", "").lower().endswith(".png"):
            has_image_attachment = True
            break

    # If no image file attachments are present, return an error message
    if not has_image_attachment:
        return {
            "success": False,
            "error_message": "One image file attachment must be present."
        }

    # If one or more image file attachments are present, return a success message
    return {"success": True, "message": "Email parsed successfully."}
```

The interesting thing for this first implementation is that because we had been talking about image attachments, it gave me code which already handled different types of image extensions. This was good but it is against the TDD philosophy of writing just enough code to pass the test. I decided to leave it in however.

Personally I don't find this code readable, and for the future it is likely the code will accept some extensions and not others, so we can ask ChatGPT to refactor it to use the `split` command and the `in` operator.

### Running the test

The moment of truth... does this work? I ran `pytest` and got the following error:

``` bash
E       fixture 'email_with_no_file_attachments' not found
```

Hmmm... why? Well, it turns out that the test code generated by ChatGPT had used the pytest 'fixture' style to write the tests, but it had been implemented incorrectly. It's possible that this style is too new for ChatGPT or it just didn't know how to do it. But it is something I had to dig into and fix, which took about an hour.

After fixing that, hey presto, test passed! The question remaining is: considering the time it took to fix the error, would it have been faster for me to write this myself?

## Test 2: The Success Case

This is a more complex case so I knew this would be a challenge to ChatGPT. At least it would be an interesting experiment.

The key point here is that I wanted to model the software engineer's task of extending an existing function with new logic. Software engineers do this every day and I was wondering how to achieve this in ChatGPT without it simply producing new functions.

### Writing the Test Case

I gave a similar prompt with the new BDD specification (already described above), but this time I specified the input argument type for the function being tested, so that it would conform to the existing function.

Curiously, this time I got a pytest-bdd test so I didn't have to ask for a correction. The other interesting point is that it recognised that the BDD specification tested for files to be saved, which was not a very functional thing to do (it is a side-effect and difficult to test). I received a small lecture from my AI pair programmer that this was not preferable. This is of course correct, and I had intentionally kept the BDD test as it was to see what the output would be, and the output was surprisingly good.

### From BDD to TDD

At this point I realised that there is a key transition that happens here, which is that BDD focuses on system-level behaviours whereas TDD operates at the function level. This transition is not very well-defined and is usually left to the skill of the programmer; their code should ultimately satisfy the BDD requirement (with an automated test), but also be decomposed with appropriate unit tests.

I decided to see if ChatGPT could assist with this type of decomposition:

```
Given the BDD scenario:

<same scenario>

Provide a suggested sequence of python function specifications which could implement this scenario.
```

I won't take you through the actual responses and the refinement process. Instead here are the key points.

![Pair Programming Robot](./images/aitdd/pair-programming-with-robot.jpg)

#### First pass: Too Many Functions

The response initially advocated implementing one function for every component of the email (subject, body, attachments), and then to save the requested outputs individually. While this does make small, easy to test function, it has three problems for me.

   * It requires further functions to assemble and process all the extracted information. For a typical programmer I think this is too fine-grained, and implementing a single function is preferable.
   * Multiple small parsing functions will require parsing of the whole email (or at least parsing of parts of it) multiple times, which is not an efficient solution.
   * TDD advocates writing 'just enough code' to make the test pass, and this seems like too much code.

This is of course mostly my opinion, but I think it is a fair one for code maintenance and readability. I asked ChatGPT to reduce the number of functions and provide one function for parsing the email.

#### Second pass: Function signatures

The next response suggested function signatures which returned tuples. Tuple return types, in my opinion, are harder to follow than a dictionary or object which have intrinsic labels. I asked ChatGPT to switch the return types to objects.

#### Third pass: Incompatible with existing design

I now had a suggested parsing function signature which took an email as a text string and output an object (or `NamedTuple`) with fields reflecting my BDD requirements. Great, but now I noticed something which I think will be key to using these tools effectively: It conflicted with the function I had already written (in Test 1). Previously I decided (on the AI's advice) to separate de-structuring the email with parsing the contents according to our specific app requirements, but now ChatGPT is suggesting a different process!

I think this will be a recurring issue with using a tool like this; ChatGPT is not a member of your software team, so it does not have consistent access to ast decisions or to your existing module, although you can pass the code to it as input (however I think this raises a whole set of questions over IP protection).

I think a developer or engineer using ChatGPT will always be struggling with this, because we all know that that vast majority of a developer's work is to extend and enhance existing code. If every developer on your team generates code like this, then who knows what state your codebase will end up in. The cynic in me predicts stand-up meetings in which developers defend 'their' ChatGPT's decision over the others.

#### Final outcome

After some further direction, ChatGPT provided the following test. I ultimately needed to instruct my AI coding partner to write a test which conformed to specific inputs and outputs, thus satisfying both my BDD requirement and the existing function signature.

``` py
def test_parse_email_data():
    content = """
        --- POST TEXT
        This is the post text
        --- CAPTION
        This is the caption
        ---
        """
    attachments = [
        {
            'name': 'File1.jpg',
            'content': 'attachment content'
        }
    ]
    expected_output = {
        'success': True,
        'post_text': 'This is the post text',
        'captions': ['This is the caption'],
        'attachment_content': ['attachment content']
    }
    assert parse_email(content, attachments) == expected_output
```

### Implementing the code

Implementing the code which passed this test was the most enlightening. I gave ChatGPT my existing function (that it had written for me previously) and the above test, and asked it to modify the existing function to make the new test pass.

The output was very sensible and added code which parsed the email content and looked for the input delineation markers, but it was wrong.

``` py
def parse_email(content, attachments):
    # Extract post text and captions from email content
    post_text = ""
    captions = []
    for line in content.split("\n"):
        if line.strip().startswith("--- POST TEXT"):
            post_text = line.strip().replace("--- POST TEXT", "").strip()
        elif line.strip().startswith("--- CAPTION"):
            caption = line.strip().replace("--- CAPTION", "").strip()
            if caption:
                captions.append(caption)

    # Remainder of the function unchanged...

    # Return post text, captions and attachment content
    return {
        "success": True,
        "post_text": post_text,
        "captions": captions,
        "attachment_content": attachment_content
        }
```

Running the tests that I provided to it immediately revealed the failure, and you can see with not much effort that the new parsing logic does not actually parse text of the form:

```
--- MARKER
data
--- MARKER
data
---
```

It instead tries to parse text of the form:

```
--- MARKER data
--- MARKER data
```

I was able to improve it with some more prompt wrangling but I realised I was spending more time prompting than solving the problem. I eventually gave up working at this level and implemented this code myself using a reducer:

```py
    # Define an reducer function
    def rfunc(total, line):
        # Update the key according to the next captured line marker
        key, d = total
        if line.startswith("---"):
            # Update key
            key = line[4:].strip().lower().replace(" ","_")
        elif key:
            # Perform an update
            d[key].append(line)

        return (key, d)

    lines = map(str.strip, content.strip().split("\n"))
    body_dict = reduce(rfunc, lines, (None, defaultdict(list)))[1]
```

(Curiously I showed this code to ChatGPT and it said that it did indeed meet the requirements!)

Once again this is subjective, but I believe this code:

 1. is easier to understand, as it defines a clear function which is applied to each line
 2. is more efficient, using a `reduce` function to only iterate once through the input
 3. it is easier to read, since ChatGPT tended to output many long-winded if-then-else statements


![Abstract AI](./images/aitdd/ai_brain.png)

## Conclusion

This was a valuable experiment with many new things learnt about using ChatGPT in this way. The most interesting one was the transition from BDD to TDD. It is probably difficult for many developers to do, and directing ChatGPT to make this transition was far from smooth.

The main benefit I found was that it prompted me to think more about design decisions - it did almost feel like I was 'pair programming'. However I was hoping that I would be able to continue thinking at a high level, but that didn't happen; because some of the output had mistakes or was poorly written (in my opinion), I had to jump between design-level and code-level thinking.

This raised an interesting question though - does this in fact fit into the TDD 'Red-Green-Refactor' process? Maybe it does and I have just been executing the 'refactor' stage a bit too early? I admit I sometimes neglected to wait to see if the code that was produced passed, thus following the 'write the minimum code to turn the test green' rule.

My other conclusion is that using this process to complete an entire BDD feature is tricky and potentially laborious, because the LLM has to maintain knowledge of existing code. Making frequent small tweaks to an existing function using an LLM may be more work than doing it yourself. Additionally, after further use I found that on occasion it would introduce errors into existing code, providing more work for the developer to do. As the function size increases, I think both of these will be exacerbated.

Other associated points are:

  - defining the expected inputs/outputs for unit tests is a bit laborious
  - Some responses introduced assumptions in the details (e.g. I asked it to use URL-encoded-strings and it used outdated formats which I had to fix)
  - The output is often verbose, leading to lengthy, duplicated or redundant code. This was especially true when parametrizing tests.

Some of these may be improved in GPT4, we will have to see.

The most concerning thing for me was that after handing so much control over to the AI, I found myself with much less understanding of the final function than I would usually expect. The question is, is this human-level understanding still valuable when AI can understand for us? I think it is, for we can only think critically and creatively if we can first understand, and I don't think these qualities should be taken away from us just yet.
