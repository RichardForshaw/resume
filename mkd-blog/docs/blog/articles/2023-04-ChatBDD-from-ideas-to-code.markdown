---
layout: post
title:  "ChatBDD: AI-Assisted Behaviour-Driven Development"
description: "AI such as ChatGPT can act as a highly productive assistant and may even help the way that you think. But can it help turn a customer idea into a piece of working software?"
tags:
    - Programming Techniques
    - AI
    - Agile
author: Richard Forshaw
---

In embarking on a new side-project, I was faced with writing code again. I love writing code, but it certainly takes mental effort. I have noticed that writing entire modules on my own requires me to think about multiple things and draw an many areas of experience, from test design and using the core language libraries (in this case Python) all the way up to trying to keep the overall goal and high-level architecture in mind. And at the same time trying to keep things simple.

I came across a post on LinkedIn which talked about using ChatGPT in writing tests vs writing code. I had used it briefly to both write some tests and code for me, but not really the two together and not really in any structured fashion. Being the master of my own idea, I am in the position to define the high-level outcomes and ultimately direct the functionality of the code so I wondered how much of the BDD/TDD process could be improved by using an AI assistant.

Usually in this situation I would simply start coding (tests first of course), but sometimes I would fail to stick to a clear coherent path, instead getting lost in a sea of ideas due to my excitement in how amazing the new system would be. So could I use ChatGPT to help me focus?

Let's find out.

![BDD meeting with a robot](./images/aitdd/three_amigos_and_robot.jpg)

## The Method: From behaviour to code

I decided to take this approach:

 1. Define the intended outcome of my module in order to write scenarios
 2. Use each scenario to turn into tests
 3. Use the tests to write the code

I believe there is a huge benefit of using ChatGPT to do this, especially point 3, because as humans sometimes we can't help but be creative, but TDD dictates that once you write the test you should write the code to make it pass and ONLY enough code to make it pass. Thus using ChatGPT makes it easier to stick within this pattern.

## Define the outcomes

When I was consulting, there were two key outcomes that I looked for when preparing for a sprint: defining the general desired behaviour and providing specific examples. This typically meets a 'definition of done', in that the general behaviour of the system is described and there are some testable examples which allow the developers to ensure that the code that they have written meets some specific testable criteria.

I started off asking ChatGPT this:

```txt
You are an expert business analyst with additional expertise in Software User Stories and BDD. You help turn business requirements given as User Stories into multiple BDD Given-When-Then scenarios.

A User Story is of the format:
As a (user type)
I want to (perform an action on the system)
So that (I meet a desired outcome)

A Given-When-Then scenario is of the format:
Given (an initial context)
When (an event occurs)
Then (a testable outcome is satisfied)

---

I am writing a software module which accepts an email from a user and extracts the components so that they can be used to post to Instagram. The user story is:

As an Instagram user,
I want to send an email to 'The System' which contains an image and some text
So that the image and text are extracted in a way that it can be posted to Instagram

Write BDD scenarios which meet the user story.

```

To my amazement, ChatGPT output the following:

``` properties
1. Scenario: Email with image and text is successfully processed
   Given the email contains an image and some text
   When the email is received by 'The System'
   Then the image and text are extracted from the email
   And the image and text are formatted for Instagram posting
   And the formatted image and text are saved to a file

2. Scenario: Email with no image is received
   Given the email contains no image
   When the email is received by 'The System'
   Then an error message is returned
   And the email is not processed further

3. Scenario: Email with no text is received
   Given the email contains no text
   When the email is received by 'The System'
   Then an error message is returned
   And the email is not processed further

4. Scenario: Email with an image that cannot be processed is received
   Given the email contains an image that cannot be processed
   When the email is received by 'The System'
   Then an error message is returned
   And the email is not processed further

5. Scenario: Email with text that exceeds the character limit is received
   Given the email contains text that exceeds the character limit
   When the email is received by 'The System'
   Then an error message is returned
   And the email is not processed further

6. Scenario: Email with an image that exceeds the size limit is received
   Given the email contains an image that exceeds the size limit
   When the email is received by 'The System'
   Then an error message is returned
   And the email is not processed further

7. Scenario: Email with unsupported image format is received
   Given the email contains an unsupported image format
   When the email is received by 'The System'
   Then an error message is returned
   And the email is not processed further

8. Scenario: Email is received from an unauthorized email address
   Given the email is received from an unauthorized email address
   When the email is received by 'The System'
   Then an error message is returned
   And the email is not processed further

9. Scenario: Generated Instagram post is successfully saved to file
   Given an image and text are formatted for Instagram posting
   When the formatted image and text are saved to a file
   Then the file is saved successfully

10. Scenario: Generated Instagram post fails to save to file
   Given an image and text are formatted for Instagram posting
   When the formatted image and text are saved to a file
   Then an error message is returned
   And the file is not saved successfully
```

What a start! I am usually able to come up with reasonable failure scenarios, and the first thing I noticed was there were scenarios here which I hadn't even considered yet, for example the character limits and attachment size limits.

The fact that this was generated in about a minute should not be overlooked. I estimate that this would take me about half and hour to think of an type up. So we are looking at an incredible speed-up.

![Writing effective use cases](./images/aitdd/cockburn_usecases.jpg)

Examining the output, there were a few things that for an MVP I did not consider important since I would be the only user (un-authorised email addresses and image format). There were also some things which were missing, probably due to some vagueness in my starting story. So I asked for some refinements:

```txt
Please make the following changes:

 1. The image is received as an attachment and only one attachment is allowed.
 2. The outcome is not a formatted image. The outcome is that the image is extracted and saved, and the text is extracted and saved in a suitable format for subsequent processing.
 3. The text in the email can specify multiple image captions and a carousel caption.
 4. The product is an MVP and so scenarios 6, 7 and 8 are not required
```

I will spare the duplication, so here are the updated scenarios that it created:

```properties
1. Scenario: Email with one image attachment and text is successfully processed
   Given the email contains one image attachment and text
   When the email is received by 'The System'
   Then the image and text are extracted from the email
   And the image and text are saved in a suitable format for subsequent processing

2. [unchanged]

3. Scenario: Email with more than one image attachment is received
   Given the email contains more than one image attachment
   When the email is received by 'The System'
   Then an error message is returned
   And the email is not processed further

4. Scenario: Email with text specifying multiple image captions and a carousel caption is received
   Given the email contains text specifying multiple image captions and a carousel caption
   When the email is received by 'The System'
   Then the image captions and carousel caption are extracted from the text
   And the captions are saved in a suitable format for subsequent processing

5. Scenario: Extracted image and text are successfully saved
   Given the image and text are extracted from the email
   When the image and text are saved
   Then the image and text are saved successfully

6. Scenario: Extracted image and text fail to save
   Given the image and text are extracted from the email
   When the image and text are saved
   Then an error message is returned
   And the image and text are not saved successfully

```

Hmm... ok, so it removed 6, 7 and 8 as requested, but it also removed scenario 3, 4 and 5 which was weird. This then drew my attention to the fact that scenarios 5 and 6 were not really saying much. I decided to keep scenario 6 because maybe there would be an internal fault which is a fair test case, but scenario 5 is basically the same as scenario 1.

I have found that directing existing output from ChatGPT can be tricky and frustrating, but I could still hand-pick the best of all the outputs. However these scenarios are still quite high-level - what about that missing detail? I decided to try another approach.

## Refinement: Example Mapping

When I was introduced to Example Mapping I loved it. As a developer, if given a detailed user story or requirement, I always found myself thinking of examples to test and often found that I was unable to think of them or that they were incorrect because of a misunderstanding. The lack of example could be fixed mid-sprint by talking to a stakeholder, but incorrect scenarios would not usually be found until the end of the sprint.

Example Mapping seeks to change this, and involves stakeholders, developers and QA discussing the scenarios to define examples of what they mean. Usually this gets off to a rocky start simply because these people don't often talk to each other! But after a short while I often saw a flood of enthusiastic discussion pour forward.

The scenarios from the first experiment may already look complete, but they use language such as 'an error message is returned' which is not specific or testable. In order to get more detail from ChatGPT, I decided to put it in an Example Mapping scenario instead. Since I could wear at least 2 of the caps from an Example Mapping meeting, I could direct ChatGPT to write some examples. I used the [rules for Example Mapping](link) together with the rules for BDD scenarios and pushed through the user story with some more request details.

```txt
You are a software product specialist with knowledge of BDD, User Stories and Example Mapping. You are participating in an Example Mapping session. This session follows these rules for a given user story:

Start by writing the story under discussion on a yellow card.

Next write each of the acceptance criteria, or rules that we already know, on a blue card.

For each rule, we may need one or more examples to illustrate it. We write those on a green card and place them under the relevant rule.

Examples are written in the BDD Given-When-Then scenario format as follows:
Given (an initial context)
When (an event occurs)
Then (a testable outcome is satisfied)

As we discuss these examples, there may be questions that nobody in the room can answer. Capture those on a red card and move on with the conversation.

---

Take the following user story:

As an Instagram user,
I want to send an email to 'The System' which contains an image and some structured text
So that the image and text are extracted in a way that it can be posted as an Instagram post or carousel

Take the following rules:

1. The email must contain 1 image file attachment
2. The email must have a subject "INSTAGRAM POST <date>"
3. The email must contain some body text
4. The body text must be structured to create either a single image post or a carousel post of 2 or 3 images
5. The structured body text must contain a general post caption and a caption for each desired image in the post
6. Error messages are returned as a HTTP 400 code with an associated message

Write the examples as per an Example Mapping session, and also write any unknown questions.

```

I shan't bore you with the text output - instead lets put them onto cards as they would be in a real Example Mapping session. Unfortunately image generators are not good at producing text, so this one is a manual effort - please excuse any poor formatting as some output was quite long.

![Example mapping result](./images/aitdd/AI_Example_Mapping_1.png)

At first glance, this looks pretty good, and once again it only took about a minute to produce it. However there are some issues, and in a real session I wouldn't let this out of the room. Let's look at the positives first.

 - ChatGPT correctly structured the cards (in the text output the examples were correctly aligned under the rules)
 - ChatGPT did make examples according to the rules, and distinguished between input scenarios
 - The additional questions blew me away - they are all valid: attachment naming, additional body text and receipt address

Now the negative:

 - The user story outcome has again been interpreted as posting to Instagram, when it is not
 - The failure scenarios are testable but the success scenarios are not really testable. I prefer examples describing outcomes which can be translated almost directly into a test.
 - The carousel scenario is missing a test for 3 captions
 - The carousel scenario is missing a failure case for more than 3 captions

Now, you can say that these are because it has not been given sufficient direction (again). In the first two points this is perhaps true, but in the final two I think there is enough information for a human to have understood (like the rule for images). But this is often what is discussed in Example Mapping meetings.

Since this is an experiment with ChatGPT, let's try again with more direction, and answer some of the questions. Here is the updated request and rules:

```txt
Take the following user story:

As an Instagram user,
I want to send an email to 'The System' which contains an image and some structured text
So that the image and text are extracted and stored so that it can be later used to generate an Instagram post.

Take the following rules:

1. The email is addressed to "me@postrobot.com"
2. The email must contain 1 image file attachment and can have any name
3. The email must have a subject "INSTAGRAM POST <date>"
4. The email must contain some body text
5. Body text containing "POST TEXT" and "CAPTION" labels create a single image post
6. Body text containing "POST TEXT" and "CAPTION-1"..."CAPTION-N" labels create a carousel post
7. A carousel post contains no more than 3 images
8. Text extracted from the email is stored as JSON, containing the date, post text, captions and image name
9. Error messages are returned as a HTTP 400 code with an associated message

Write the examples as per an Example Mapping session, and also write any unknown questions.
```

For brevity, I will spare the detailed output, but below are the key results from the response:

 - The output now only contained a positive example scenarios, whereas previously it also contained negative ones
 - Because there were no negative scenarios, the only output involving an error (responding to (9)) was "Then a HTTP 400 code with the associated message is returned", which was not helpful
 - Some of the questions it now raised had already been deduced in the previous attempt, e.g. now it raised the question: "What happens if there is no image attachment in the email?". I think a human would have deduced this from rules (2) and (9)

![Hitting the target](./images/aitdd/archery-target.jpg)

## Conclusion

Partnering with ChatGPT to expand a user story into testable scenarios once again showed how a LLM such as this is very useful from a general stand-point but not from a detailed one. On the positive side, all the answers above were obtained in seconds, meaning I spent more time analysing the results and looking for errors than typing the prompts and waiting for output.

All in all I probably only spent a few minutes actually interacting with the system. It gave impressive results to allow me to build up a list of scenarios to consider, and also questions that I might have missed. So in a sense, it acted very well as a team-mate.

The problems exist when searching for detail. Perhaps I am picky, but some of the output was not useful to move forward with. Using ChatGPT for high-level behaviour was good, but any thought of straying down to any level of detail left me disappointed. If it is common to re-prompt with more detail, then I might as well just add the detail myself.

I also found a lack of consistency between prompts. It mostly performed well but it forgot previous outcomes enough to frustrate me. If I saw this behaviour in a software developer working on my team, it would annoy me.

Perhaps this is expected - after all LLMs do not 'think', they simply perform highly-advanced statistical pattern-matching. For many purposes this is sufficient and provides plenty of useful responses and food for thought. But at the moment it takes a human to go that step further. (Note that this was done on ChatGPT3.5. Perhaps GPT4 goes further).

Overall, ChatGPT gets top marks as a productivity assistant. I suspect that the swift generation of output, with a little extra consideration on the inputs, would save a lot of time in the real world, if not simply for automating the output of boilerplate text. So I can see a huge benefit.

That is enough for this post. What about translating the scenarios into code? Head over to [Part 2...](./2023-04-ChatTDD-pair-programming-with-ai.markdown)

