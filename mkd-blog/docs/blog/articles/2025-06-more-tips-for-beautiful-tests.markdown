---
layout: post
title:  "Beautify Your Tests and Test Better!"
description: "Depite having many tests, testing is still difficult and encouraging TDD is harder. When an old test breaks, knowing what has happened is difficult. By beautifying our tests, we made testing easy and fun again!"
tags:
    - Software Development
    - BDD
    - Testing
    - Python
author: Richard Forshaw
---

I wrote recently about how [creating a domain-specific test language](../articles/2024-05-beautiful-tests-better-tests.markdown) can make your tests more readable, easier to maintain and understand, and hopefully more pleasurable to write.

Having spent more time on improving the test suites at Instatruck, I have come across some more patterns which seem to improve the comprehension of tests and understanding what the testing intent is. So without further ado, let's check them out!

![Communication](./images/two_heads_communicating.png)

## General philosophy: make it obvious

As I mentioned in my previous post, the most important thing in writing a test is not testing the functionality is correct (although, it is still essential!). The most important thing is ensuring that the *intent of the test is understood*, and can be understood quickly by anyone, from your product owner to your junior developers.

You may ask why? After all, when I am writing a test (and hopefully it is being written [before the code is written](https://martinfowler.com/bliki/TestDrivenDevelopment.html)), I know the context of the test and what the function's inputs and outputs should be, or what the system's required set-up is to test a behaviour. And once the test is written and passing then it's "job done", right?

Not really. You can say that this information is 'most relevant' at this point in the test's life-cycle, but I guarantee that for many tests in your suite there will come a time when behaviour needs to change either in that code or in related code, and one of those tests will break. First, you will be thankful (Yes! I have a test that has saved a bug getting into production!). But then when you inspect the test to understand what has happened you will turn to dispair and think "What exactly has broken? What is this test actually testing? And how is it testing it???"

Thus what you thought was a 2-hour task becomes a 2-day task.

Making intentions obvious and understandable is the way to prevent this. But this is really a tactical statement. How can we go about actually putting this into practice? Here are 4 of my suggestions.

## Tip 1: Test a Single Thing

This seems obvious and you have probably heard it before, but it bears repeating. Even when I have had to re-visit my own tests from years ago, I have come across a test that tests multiple things in one go.

This is dangerous for two reasons:

Firstly, this makes the tests misleading and less readable. Misleading because a single test failure could be a single bug, or two bugs, or 5 bugs, you just don't know. If the test fails early, then you have no idea what the remainder of the tests will do, since they have not been reached yet. They are also less readable because the tests become a mish-mash of setup, prompt, test and re-set-up. Because of the procedural style of code, it can be hard to distinguish the actual testing code without extensive use of comments.

Second, because of set-up and tear-down requirements for tests, testing multiple things in a single test function will often mean you need to re-set system state, and the way this is done may not always be reliable. Handling this in a function that tests multiple things may result in failing tests due to a change in the underlying state management of the system. This is really not a 'real' test failure because half of the things tested in the test may still work, but an unrelated change causes a subsequent test to not have its data set up correctly. You will often find that when the setup is corrected then the tests pass because nothing was really 'broken'.

A test should ideally test one thing - one function or one behaviour from one input. This can lead to a lot of tests, but it also means that when a test fails you know **exactly** which functionality is broken.

![Metamorphosos](./images/insect-metamorphosis.jpg)

## Tip 2: Given When Then

Anyone who has used [Gherkin](https://cucumber.io/docs/gherkin/reference) will recognise this format. After having used this for a few years, I think all tests should be written with this format in mind even if you don't use a gherkin-based testing library. The reason the format is so good is becasue it separates the test into 3 important parts:

 1. **Setup**. 'Given' the system is in a specific state which is directly related to the test.
 2. **A trigger or event**. What is the thing that should be triggering the behaviour? Typically in a web-based system this is a user action, or in the case of an API it is an API call (often from a user action)
 3. **Expected result**. What should the user see or the system output when this event happens?

At Instatruck we went through multiple stages in achieving this:

 - First we simply organised the test code in 'blocks' in the test functions with some explanatory comments. This at least allowed a reader to know what was setup, what was the event and what the expected results were
 - This then made it easier to identify common code or behaviour, which allowed us to refactor these into supporting functions with meaningful names (like `given_a_driver_is_logged_in(user_object)` and `when_a_new_job_is_posted(job_data)`)
 - Finally, patterns could be detected across test modules and refactored to be re-used from a common domain-language library.

This last point then brings me to my next tip...

## Tip 3: A Domain-Specific Test Library

It was at this stage in maturing Instatruck's testing abilities that inspired [my other testing post](../articles/2024-05-beautiful-tests-better-tests.markdown) about domain-specific test languages. Creating a test suite like this has a few benefits:

 1. You can write tests almost like plain English
 2. You can use the same language as you use in your feature specifications (especially if they use Gherkin)
 3. You can abstract multiple system and setup functions in one user-level statement.
 4. These statements become consistent across the whole test suite which aids in comprehension

At Instatruck we chose to mimic the Gherkin scenarios by using object-chaining. For example, you could re-write a `when_a_new_job_is_posted` function mentioned above as:

```python
test_job_spec = Given.a_job_for_a('Van').starts_at(configured_address_1)._and.goes_to(configured_address_2)
When.the_user(user_obj).requests_job(test_job_spec)
```

This can then be re-used by many different test in a standard way across the whole test suite.

![Multiplication Table](./images/multiplication_table_toy.jpg)

## Tip 4: Declarative Tabular Parameters

I am a big fan of declarative programming, especially when using classes and objects. I think that declaring object behaviour is a more effective and useful way of writing functions that implement the same thing. There are a few reasons for this which I hope to write in another post, but one of them is seeing the behaviour defined in one easily readable place. Django and the Django Rest Framework does a good job of using a declarative style by allowing the user to declare what models a view uses, what sorting or filtering class it uses, what permissions it has and many other things.

How does this translate to writing good tests? By **declaring a table of expected behaviours or outputs**. At Instatruck we have used the [parameterized](URL) library for a long time which performs this function well. For example, not only can you use a table-format to test types of input:

```py
    @parameterized.expand([
        # Test Format,              'after' filter time,            'before' filter time
        ("ISO 8601",                "2025-01-01T01:00:00",          "2025-01-03T01:00:00"),
        ("Fractional Seconds",      "2025-01-01T02:00:00.321235",   "2025-01-03T00:00:00.321235"),
        ("Datetime with Hour/Min",  "2025-01-01T01:22",             "2025-01-03T01:44"),
        ("Date Only",               "2025-01-01",                   "2025-01-03"),
    ])
    def test_get_break_list_with_different_datetime_format_filter(self, _, after, before):
        # ...
```

You can use it to make readable testing-tables with inputs and outputs that can be verified by the business:

```py
    @parameterize.expand([
        # Truck Type, load kg, length cm, expected charge rate
        ("Ute",         100,        200, 'Vans and Utes 1t'),
        ("Ute",         500,        200, 'Vans and Utes 1t'),
        ("Van",         500,        150, 'Vans and Utes 1t'),
        ("Van",         1000,       150, 'Vans 2t'),
        ("Van",         2000,       100, 'Vans 2t'),
        ("Pantech",     2000,       100, 'Flatbed & Pantech 5t'),
        ("Pantech",     2000,       400, 'Flatbed & Pantech 7t'),
        ("Pantech",     6000,       200, 'Flatbed & Pantech 7t'),
        ("Pantech",     6000,       500, 'Flatbed & Pantech 9t'),
        ("Pantech",     1000,       500, 'Flatbed & Pantech 9t'),
    ])
    def test_selects_correct_charge_rate_from_load(self, truck_type, weight_kgs, len_cm, expected_rate):
        #...
```

We have found that structuring tests this way conveys so much more information to so many people, that we are able to look at tests and understand their intent very easily, so much that non-technical staff can look at the test table and know how the system is behaving (and tell you if it is wrong).

## Next Step: BDD

As we are slowly introducing the [python-bdd](URL) library into some systems, which will allow us to move these declarations into the actual feature-file scenarios. These are test scenarios that are written and stored in plain text files (using Gherkin) and then interpreted by testing libraries. These can also include tables. For example:

```
Scenario: Approving a driver document type which is already approved
  Given there is a driver in the 'On-Boarding' state
  And the driver has a <type> document with ID 10 in the 'approved' state
  And the driver has a <type> document with ID 20 in the 'New' state
  And I am logged in as Admin
  When I 'approve' document with ID 20
  Then I see a message "There is already a <type> document in the 'approved' state for this driver"
  And document ID 20 is still in the 'New' state
  Examples:
    type
    Medical
    Driving License
    Goods Insurance
```

These files can then be shared with, reviewed by and even updated by non-technical team members, and then almost immediately tested again, allowing a faster exchange of information and faster system development times.

So don't treat your tests as second-class citizens. Your tests can be transformed into an effective layer of communication between the tech team and the product team, and also improving understanding between your current and future developers. Embrace it!