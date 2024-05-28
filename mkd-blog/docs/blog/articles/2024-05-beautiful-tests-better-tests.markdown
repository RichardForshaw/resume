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

At [Instatruck](https://www.instatruck.com.au), we are fortunate to have over 2000 automated tests, built up over many years. This lends a great degree of confidence when extending code. But while automated testing carries many benefits, there are also some hidden costs.

When you dip into these tests, perhaps to add new functionality to an old class or module, it is easy to see how much the testing 'language' has evolved. Early tests, especially complex ones, are terrible to read and understand. API calls are inconsistently mixed with internal calls, mocks are everywhere (a code smell of poor design), test functions cover multiple test cases. But most importantly, beyond a hopefully well-named test function, it is sometimes difficult to know *what* is being tested.

Recently, I had had enough. What could I do to improve this?

![Test Tubes](./images/test-tube-closeup.webp)

## More people more problems

When working with a team, this problem is only made worse. Firstly, other team members will be less likely to understand what is being tested since they are not the original authors of the tests and also may have little experience with the code being tested. Because of this, they will sometimes come up with their own 'ways of testing'. These new ways are usually better than the old ways, but they often come with the same problems wrapped up in a different coding style.

If the testing method is not clear to see in the existing tests, then you will continue to get two major problems:

 1. **Old tests will be difficult to understand**. If new code breaks an old test, it is important to be able to communicate quickly what *behaviour* the new code has broken. This does not mean knowing what function or functions have stopped working, but what high-level behaviours, intentions or rules have stopped working. It is better to understand the behaviour that is not working than the internal function that is failing.
 2. Because the **testing methodology is not clear**, new developers will write new tests with their own methodology. This then causes item (1) to spread and results in a loop which gradually decays the readability of the tests and the productivity of the development team.

Here is an example of old testing code that is starting to show its age. To keep this post simple, it is not a complex example which shows the worst habits, but it could certainly be better. (Comments added are mine)

```python
    def test_truck_type_information(self):
        ''' A list of truck types and information are provided '''
        response = self.client.get('/api/public/truck_type_info/')

        # Developers need to know all these assert methods
        assert_jok(response)
        assert_equal(TruckType.objects.count(), 7)  # Behold a 'magic' number
        assert_length(response.data, 3)             # Behold another 'magic' number

        # Developers need to know the structure of the response every time they test it
        truck_type_names = [r['name'] for r in response.data]
        assert_list_equal(truck_type_names, ['Ute', 'Van', 'Pantech'])

        # Again, developers need to know internal structure,
        # and know how to programatically access them
        field_names = set([i[0] for i in response.data[0].items()])
        assert_list_equal(sorted(list(field_names)), ['description', 'id', 'image_url', 'name'])

```

My main bugbear is that this is bare-metal test code, which needs the comments in order to explain it. There is no re-usability here and you generally need to read the code and the comments to understand the testing intent. But there is more harm lurking beneath. Have any of these crossed your mind before?

 * Developers **need to know implementation details** in order to write tests. We develop in Django, and so we have to remember to access `response.data`, which is returned by the framework. We also develop with Rest Framework which gives different response structures for item-retrieval and list-retrieval, which you need to remember when writing tests. Developers usually lose time just remembering which structure to use.
 * Developers need to **know the assertion methods of the testing library** you use. Some of them may be customised and not clear as to what they test, so these methods tend to just be copy-pasted when writing new tests 'just because they are in other tests'
 * We recently tried to migrate to a new test framework. It was so hard we gave up. The reason it was hard was because these **assertion methods are everywhere** and the changes required to migrate them was too big, even when using migration tools. Having your assertions spread out like this tends to lock you into a test framework.

 ![Given When Then](./images/given-when-then.jpg)

## Gherkin to the rescue

I have long been a fan of BDD and Gherkin scenarios. This is because of 2 reasons:

 1. They deal with system behaviour, so they really deal with *things that are important to the customer*
 2. They are written very close to *plain english*

The other benefit of using a gherkin-style is that it splits test scenarios into 3 distinct sections:

 1. The *Given* section, which sets up the context of the test
 2. The *When* section, which describes the event that happens to the system
 3. The *Then* section, which describes what should happen, i.e. the testable outcome

I have seen a video in YouTube which simply advocates for arranging your test functions into these 3 clear sections, and I wish I could find it again. However Dave Farley does have comprehensive videos on BDD testing such as [this one](https://www.youtube.com/watch?v=gXh0iUt4TXA) which use this structure.

BDD test frameworks use this style but I haven't been totally impressed when using them (in Python at least). Yes they do force you to arrange your code into blocks which align with your Gherkin scenarios (and also 'compile' them against your feature files so you can determine your feature coverage). But within these blocks  you are still allowed free reign to write tests how you like them. This can often lead to problems with reusability of common code.

We started using the basic Gherkin 'step readability' concepts when writing new tests and update old ones when the opportunity arose. To continue the above example:

```python
    def test_truck_type_information(self):
        ''' A list of truck types and information are provided '''
        given_number_of_truck_types_in_database(7)

        when_the_user_requests_url('/api/public/truck_type_info/')

        then_check_number_of_expected_results(3)

        then_check_the_results_contain_truck_types(['Ute', 'Van', 'Pantech'])

        then_check_the_results_contain_fields(['description', 'id', 'image_url', 'name'])

```

You can see that this is better. The test is more readable, the 'magic' numbers now have some extra context and the intent of the test is more clear.

The main remaining problem is that of re-usability. We started doing this for a few months but with a lack of senior guidance. The result was that these BDD-style 'helper' functions were all written in the local test module, and copied if they were needed elsewhere. Sometimes they were subtly changed because of slightly different data contexts.

This was obviously headed for a new disaster.

## Other language inspiration

Even though I rarely develop in Javascript, there are times when I have needed to use it, and in one instance I was exposed to the 'Mocha' framework and its usage of `should.js` and `expect.js`. I really liked the way that the assertions are styled so that the testing actions read like sentences. For example from the Mocha and `expect.js` documentation:

```javascript
// Mocha using should.js
describe('Array', function () {
  describe('#indexOf()', function () {
    it('should return -1 when the value is not present', function () {
      [1, 2, 3].indexOf(5).should.equal(-1);
      [1, 2, 3].indexOf(0).should.equal(-1);
    });
  });
});

// expect.js
expect(5).to.be.a('number');
expect([]).to.be.an('array');
expect([]).to.be.an('object');
```

You can already see how this goes a long way to solving the issue of understanding intent without exposing too many implementation details. So how could this be leveraged?

![Lemon Litmus Paper](./images/lemon_litmus_paper.jpg)

## A Domain-Driven Solution

Every software product has a domain. It has a domain language, from entities to user actions to behaviours. But software also has its own language - that of lists and fields and exceptions. I wanted to make sure that domain ideas were expressed along with software concepts in a style that made it easy to understand intents and re-use code. So I put all of the above into an in-house library.

To satisfy the BDD style I wanted, I made three classes:

```python
class Given:
    # Things for test setup

class When:
    # Things for performing actions

class Then:
    # Things for performing tests
```

I could then fill these classes with methods and properties which would allow tests to be written in a sentence-style, which could match BDD scenarios. I could use two features of objects (returning its own instance, and static factory methods) to do this. I could then ensure the methods had high-level-domain meanings, for example

```python
class Given:

    def __init__(self, *args, **kwargs):
        # Store anything in kwargs locally
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def driver(driver_obj_or_str):
        if isinstance(driver_obj_or_str, str):
            driver_obj_or_str = models.Driver.objects.get(name=driver_obj_or_str)
        return Given(driver_under_test=driver_obj_or_str)

    def has_some_setup(self, param):
        # Do something with the driver we have looked up
        self.driver_under_test.do_something_with(param)
        return self

# Now I can write:
Given.driver("Kimi Raikkonen").has_some_setup()
```

Returning to the previous examples, they can now be written like this:

```python
    def test_truck_type_information(self):
        ''' A list of truck types and information are provided '''
        Given.there_are(7).truck_types

        response = When(self).the_user.requests.url('/api/public/truck_type_info/')

        Then.the_system_responds(response).with_success()
        Then.the_response(response).contains(3).results()
        Then.the_response(response).field('[*].name').is_equal_to(['Ute', 'Van', 'Pantech'])

        Then.the_fields(['description', 'id', 'image_url', 'name']).are_present_in(response)
```

I think this is immediately better:

 * The intent of the tests is much clearer.
 * The test is grouped into a familiar Given/When/Then style
 * Shared setup and assertion code can be reused
 * The developer writing the test doesn't need to know so much about the implementation all the time, and can write tests faster.

But why write your own framework? Isn't that a lot of work? Because of the language of your domain, I think it is more difficult for software systems to use off-the-shelf (high-level) testing libraries if you want to express intent at the domain level. If you are only writing Unit Tests which deal with internal functions, then this is probably not a good solution effort-wise. But once you are dealing with domain-level concepts I think it is worth investing in a custom library.

The other plus point in my book is that _all the low-level testing methods can be migrated to your test framework_. What this means for us is that after this is done, upgrading to another test library will be much simpler, as fewer files will need changing. This is a bit like having a 'facade' design pattern.

![Kids toolbox](./images/kids-toolbox.jpg)

## Tips and Gotchas

You might notice a couple of things:

 * Why `When(self)`? This is because the Django test framework has a built-in test client that is part of the test object, we we need to pass it to the test class. This is a nuance that may be present in other backend frameworks.
 * What the heck is `field('[*].name')`? Because developers still need to know something about data formats, and because the response format forms part of the 'API specification', fields need to be present in certain locations. But writing code to access them is frustrating. So I used [the awesome `JSONPath` library](https://pypi.org/project/jsonpath-ng/) which uses the JSON Path specification. This allows paths to be encoded into strings, and developer can focus on accessing paths like this instead of writing access methods.

However this is a work in progress, and there are still some things to iron out.

 * _The format of natural language_. As you can see English is fluid... is it better to write 'Then the response contains the fields' or 'Then the fields are present in the response'? I didn't know which was better, but as I write more of the framework it is becoming clearer. It is a work in progress.
 * _There are many domain model types_, which potentially means many methods (for example, we probably need methods for `is_a_truck()`, `is_a_driver()`, `is_an_address()`). This can be laborious, but it's possible that I can use special Python language features to add methods dynamically for the test types.
 * Hiding implementation details is good, but _sometimes you need to know them_. For example, in Django there is a different response structure for a list and a paginated list, but to a test framework like this it is just 'a list'. Hiding this detail can introduce subtle bugs if you are not careful.
 * It's still a library that needs learning. I still find myself looking up which methods to use, mainly because of the first point in this list. But I expect this will improve. And I think it is still a much nicer solution than what the tests used to look like.

But overall I'm happy. I expect that all things testing will be looking up from now on.
