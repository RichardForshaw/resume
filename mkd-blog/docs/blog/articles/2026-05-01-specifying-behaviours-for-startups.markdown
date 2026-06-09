---
layout: post
title:  "The Behaviour Gap (Pt 1): Is your Tech Team Building the Right Product?"
description: "Under-defining your system's behaviour is the best way to lead to frustration, especially for startups and founders. Can we find the answer in some old and new techniques?"
tags:
    - agile
    - software engineering
    - BDD
    - startups
author: Richard Forshaw
---

Picture the scenario: You are walking into a meeting to test and accept the app for your new start-up idea. You have been working for months with an offshore development provider, but you haven't heard much from them except for some simple progress reports. You remember sitting down months ago and describing the product, and today's the day you've been waiting for.

You act as a customer, install the app and create an account. Then you choose to upgrade to a paid plan to test some features.

You decide to be sneaky and enter the details of a card you have that expired last month, just because you had a similar experience on another website last week, so you want to see that it's handled OK.

You click 'subscribe' and... you are thrown out of your account. You try to log in again but the response is 'Account suspended'.

You look over at the project lead. "What is happening here?"

"That's normal" he says.

"But I can't get into the account to fix my card."

"We implemented the requirement to 'handle' expired cards, and also to suspend accounts if there is a failed payment."

He flips to the page on the project scope, and points at:

 * "Handle expired card error"
 * "Suspend accounts with overdue payments"

"But that's not what I meant by overdue!" you protest. "And if you enter a bad card you should be asked for a different one, or given a chance to fix it!"

"Hmm... That's not what the scope says. That will take another 2 weeks work."

What??? But shouldn't that be obvious? Why does this need explaining? And why do you need to wait longer for something that works in every other website? 5 minutes in, and its already costing you more money.


## Why Behaviour is Important

Unfortunately this type of scenario is common, and happens everywhere from startups to large organisations. But it's obviously more painful for startups when budgets are limited.

We shouldn't blame ourselves for getting into this situation; humans are naturally bad at recognising how well another person has understood their ideas. When we feel like we are having a productive conversation with others, we will overestimate how much of the context in our heads we have actually communicated.

I met some founders recently who were in the midst of launching their new product, and they asked me to look over some of their scope documents. What I saw was evidence of a similar ticking-time-bombs. The documents were fleshed out with bullet points like:

 > _"User can successfully connect Stripe Account"_

This seems OK, if a little vague.

 > _"Payment failures are handled gracefully"_

Hmm... which failures? How do you know you've caught all of them? And what does 'gracefully' mean exactly? Is it a notification and a retry? Or something else?

 > _"Paid invoices sync correctly"_

This one had me scratching my head. Every invoice I've seen is different, so how can the variety of invoice contents, formats, breakdowns and currencies be covered by just one line?

These types of ambiguities are why I have been a big fan of Behaviour-Driven Development and practices such as Example Mapping. On the surface, these just seem like a different way to capture features, and that is partly correct but it is much more. A key part of the process is simply getting people in a room together (virtual or otherwise) who have different perspectives on the system, and working through examples of behaviour.

![The chasm of conversation](./images/conversation_chasm.jpg)

Sceptics say "but I know what the app needs to do... I can just write it down." This underestimates the power of discussion.

In my first ever Example Mapping session, I didn't think much would happen. It was a new system, and we were just defining basic user access. The Product Owner said that the user will sign up with a username and password.

"What type of password?" said the QA representative.

"What do you mean?" asked the Product Owner. "It's just a password."

"How many characters? Any requirements for numbers or capitals?"

"I don't know...". The PO looked dumbfounded. "I suppose so?"

"Great", I said as it appeard the conversation was stalling, "Let's get an answer from your head of IT and move on."

"How does the user know this?" asked our developer.

"Great question" I said, looking at the PO. "If the user needs to meet some password requirements, they should probably know what they are!"

And on it went... after about 30 minutes, we had agreed the behaviour on signing up, and it was much more extensive than what the PO thought it would be. That's the power of discussion.

## Going Retro

When I was working in complex safety-related systems, we often referred to the "V" model of Verification and Validation. The way of remembering each was:

> _Verification_: we are building the system right (correctly)

> _Validation_: we are building the right system

As you went down the 'V', you started with high-level system requirements and moved down into low-level modules and code. Then on the corresponding side, you tested each level of specification.

![The old V model](./images/Typical%20V%20model.png)

The 'V' model is seen as old and stuffy by some, but as with many things in the age of AI-assisted development, it it probably ready for a renaissance. If we look more closely, in the context of modern development techniques, we can spot some substitutions:

 - The Business and Operations concept is just like "User Stories"
 - The "System Requirements" are really the "Behavioural Requirements" (for which I use "Rules" and "Examples")
 - The "System Testing" becomes "Behaviour Testing"

So what do we have now?

![The new V model](./images/New%20V%20Model.jpg)

There is also an important line that can be drawn under the 2nd tier from the top. Above this line there *should be stakeholder involvement*. It is only below this line that development is fully handed over to the development team. The old diagram doesn't specify this, and the whole 'V' is often mistakenly seen as being 'owned' by the engineering team and not shared with the business stakeholders. This is a big mistake.

## Let's Get Real

It's all well and good talking about processes and updating diagrams. But what does this mean?

Going back to our original examples, how would you 'fix' the problem of handling an expired credit card. As with all examples, they can feel a little forced, but here is an alternative way of describing them.

#### The User Story

> As a user,
> I want to be able to subscribe using a credit card
> So I can pay easily and conveniently

> As a business owner,
> I want to charge money fairly for the use of the service
> So that the business is profitable

These seem like reasonably high-level User Stories, which need to work together. If a user is using the service, then the business owners want to get paid, and the user wants to pay in a convenient way. The key thing to realise is that these are starting points for the discussion.

#### The "Example Mapping" Meeting

This is typically where a session to decompose the stories into rules and behaviours is necessary. As highlighted before, _discussion is key_, and the parties involved should not be afraid to ask questions. This is the purpose of an ["Example Mapping" meeting](https://cucumber.io/blog/bdd/example-mapping-introduction), and I would expect questions to be raised like:

 * _"What if the credit card is incorrect or expired?"_
    - "Then the user should be told there is an error."
 * _"And what would happen then?"_
    - "They can try again or cancel"
 * _"What happens when they cancel?"_
    - "They revert to the free plan"
 * _"What about if a payment fails on an existing subscription"_
    - "Then their account is suspended"
 * _"You mean they will log in one day and have a suspended account?"_
    - "You're right, we should give them warnings if we know their card is about to expire"
 * _"How many warnings?"_
    - "Weekly from one month before"

Bringing an inquisitive mind to a discussion like this should serve to clarify many of these issues, and bring about a tight set of rules and examples. Every issue raised here is a question or assumption that is avoided once the development team starts work, and an opportunity to synchronise your expectations.

![An architectural blueprint being approved](./images/Approved_Blueprint.jpg)

#### The Outcome

I won't go through the mechanics of an Example Mapping meeting, as they are often run very differently. But the important thing is the outcome.

For me, the developers are the gate-keepers, and they should be able to declare that _a feature is ready to start development_. The simple rule to follow is that the _behaviour of the feature is understood by all parties_ and there are no more outstanding questions. A great example from above is the discovery that users should be warned about a credit card which is about to expire; this should spark a flurry of new questions:

 * How often are they warned?
 * When do the warnings start?
 * Is it a email or a notification or something else?
 * What should it say?

The final question of what the notification should say may seem trivial, but it is still an assumption which will be manifested by the developer when they implement it, and it's not likely to meet your expectations. (In my personal experience, developers are *terrible* at writing messages like this!)


## AI as a Sparring Partner

With the internet replete with 1,001 uses of AI for productivity, it would be remiss of me to not include how to use AI to help with this. I've engaged with AI tools in many ways and at many stages, and they all have their benefits.

The model I have had most success with recently is the 'sparring partner', where you prompt an AI to 'grill' you on extracting the details for your scenario. The key thing to remember is to give the LLM:

 * **a clear context** of the topic; and
 * **clear outcome expectations**
 
AIs thrive within this type of structure, when they are able to fill in the gaps between a known start point (by contextual information) and end point (by a checklist of goals).

The details of this are available in Part 2 of this article, but as a glimpse, if you do it well, the result should be something like:

```
  * Tiered Hierarchy: The application must support a tiered pricing structure (e.g., Free Tier, Tier 1, Tier 2, Tier 3).
  * Billing Interval: The billing cycle is strictly monthly. For all proration calculations, every calendar month is treated as exactly 30 days.
  * Upfront Collection: Users must provide valid credit card details at the time of signing up for the trial.
  * Length: The trial period is 14 days long
  * Pre-Expiry Notifications: The system must automatically trigger transactional reminder emails to the user at two intervals prior to trial expiration:
    -  7 days before the trial ends.
    -  3 days before the trial ends.
  * First Charge Trigger: The system must withhold the first subscription charge until Day 14 of the trial.
  * ...

```

I remember spending a week writing a specification document to this standard. Now you can probably write it in a few hours.

## Wrapping Up

When kicking off a new product or feature, behaviours are important and ambiguity is risk. To make a pithy analogy, it's a "shared understanding" that greases the wheels of the development engine room. This is doubly true now that the engine room can be turbo-charged with AI.

Whether managing a tech-team for your new MVP, working with stakeholders in a large company or instructing agents on a spec-driven project, the *behaviours* are the contract that you expect to be fulfilled, and they are the best way of communicating your expectations and getting to a shared understanding.

So how can you maximise the use of AI to help achieve this? Whether a solo fully-vertical entrepreneur or non-tech founders who need to trust a development team to build their vision, the risk of feature-correction-churn is real, and there are AI techniques available to reduce this. We will explore these in Part 2!

