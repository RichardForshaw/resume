---
layout: post
title:  "BDD Distilled"
description: "Creating software is hard. If you are a senior leader you may be using BDD... or you may **think** you are using it. Is there something you're actually missing?"
tags:
    - Software Development
    - BDD
    - Agile
author: Richard Forshaw
---

As with many concepts in Software Development, we sometimes only scratch the surface. I used to fall victim to this superficial-understanding mindset. After reading the title of a blog and taking a look at the toolset, you think that you have it all figured out. Yes, there is a book out there any maybe some training courses, but you're smart, right? You don't need to read all of it...

This is how I came to misunderstand TDD, misunderstand Unit Testing and misunderstand BDD. All of these have key unshakeable concepts that are either lost in translation or are tossed aside by many of the bloggers out there, and it is to our overall detriment.

I hope to rectify this, starting here. I've struggled with getting BDD 'working' in my team and I've been doubtful that everybody really understands it or why it is good. One of the problems therefore is... probably me. Perhaps if your team don't 'get' it or it isn't really working for you, then the problem might be... you. How well do **you** understand it, and more importantly, how well do you know how to explain it and teach it?

Every now and again I revisit the BDD expert literature so that I am sure that I do understand it, and every time I find some key points that either I had forgotten or I simply find it difficult to convey to others. So let's get down to the concepts that help me the most. Hopefully they shed some clarity for you as well.

(Many of these concepts are explained brilliantly in [Dave Farley's videos](https://www.youtube.com/@ModernSoftwareEngineeringYT)... some specific links are provided at the end)

![BDD Process Drawing](./images/bdd/BDD_Process.jpg)

## It's a Process

The most important thing about getting anything done in a software team is communication. Translating from something the business wants into a set of features is fraught with danger, expecially in larger organisations.

Consider the levels of communication that a new idea has to go through to get into a software product:

  1. The board or upper management want to exploit a need in the market ("People find it hard to do their taxes, let's help them!")
  1. This then needs to be translated into specific problem for a user of your product ("People find it hard to tally up their platform earnings over the tax period.")
  1. This then needs to be translated into a feature that solves that problem and provides value ("OK, Let's create an 'export earnings' feature!")
  1. This needs to be further refined to match the specifics of the problem ("The system will be able to export a user's earnings, providing a monthly summary of earnings with tax, GST and deductable components calculated and visible")
  1. This then needs to be translated into code and tested (way too many steps here to go into!)

It's important to realise that every one of these steps is important and is solved by communication. Jumping from step 2 to step 5 may seem like an efficient shortcut, but it will result in assumptions being made about the expected feature. This is because the people with the knowledge of the customer and their needs will be operating with different contextual information compared to the people who know how the product currently works.

BDD puts a _priority on discussion_. Without discussion, facts about the expectations are replaced with assumptions, and incorrect assumtions result in rework and can result in lack of trust between the stakeholders and the team. The tools and meetings in your BDD process should be there to **facilitate** discussion and thus **generate** the tasks that are most valuable to the users.

## WHAT vs HOW

Our natural language for discussing and specifying any solution to a problem is usually HOW the solution works. It's the same when we discuss features on a system; users perform actions and requests on the system, the system performs some logical steps, a result is output. This is true for anyone who uses the system frequently - their language will be influenced by how the system works and thus how it should be changed. But when it comes to BDD, the 'WHAT' is more important than the 'HOW'. As Dave Farley suggests: _"Ignore how your software works; specify what your software does"_.

![Dave Farley explaining HOW vs WHAT](./images/bdd/DaveFarleyBDDHowWhat.jpg)

But... why?

Focusing on the 'HOW' tends to drag us down the path of system functions and results in specifying behaviour in terms of the system's interface to the user rather than the user's goals expressed in terms of the domain language. That's just a fancy way of saying that we prefer to write about how the user interacts directly with the system, instead of *what the user wants to achieve*, even if the system wasn't there.

Specifying HOW a feature works is really the job of the development team, and including these details in the specifications is too early. There could be many ways of implementing a desired behaviour, and that is up to the development team to work out; it's not the job of the business representatives. Specifying this too early might limit some creative opportunities or technical innovation available to an experienced development team.

So when you are requesting a behaviour or system outcome, stick to the WHAT.

## Avoid Implementation Detail

This is essentially an extension of the last point. Implementation detail is just another word for 'HOW'. It can be especially tempting to do this when discussing the system at the UI level, but we have to remember that what the UI looks like and how it behaves is not the user's goal; it's simply _one way of achieving what they want_. Don't confuse UI interactions with system behaviour.

Consider entering credit card details. The objective is that the credit card details are entered and stored securely in the system so that they can be used to pay for things. Specifying things like "The user selects their card type, then enters their card number, then selects the expiry month and year from a list..." is restrictive to the team implementing the UI. For example:

 - selecting a card type is largely irrelevant these days becasue it is encoded in the number. Having a rigid UI requirements means that you can't take advantage of this feature
 - there is a recent innovation which allows card details to be entered by taking a picture of it. This type of innovation would be completely excluded with detailed steps on entering credit card details
 - What about customers who have their card details stored in a digital wallet? These rigid requirements would cause them extra friction

Hopefully this is more evidence for the power of sticking to the 'WHAT' and not the 'HOW'.

![Dictionary definition](./images/definition.png)

## Use Domain-Language Examples

Picking a commonly understood and consistent language is a very important aspect to defining both problems and requirements. The language for these should be from the point of reference of the user and the problem they want to solve. If you are designing an online bookstore, then the language should involve the customer looking for and purchasing books, or the shop owner checking the inventory and pre-orders of books. If you are designing a transportation system then the language should involve the customer delivering items to locations and checking arrival times.

In BDD, you then typically use examples codify the specifications. Occasionally you might not need an example, but I try to provide them all the time for clarity because you never know when some hidden ambiguity might appear. I've been burnt a few times by assuming that you don't always need examples.The beauty of examples are that BDD aims to convert them into **Executable Specifications**, which involves implementing a test in a way that proves that the specification is satisfied.

As Dave Farley mentions: "New work starts with an executable specification". But executable specifications also serve another purpose - providing a **Definition of Done**. The product owner should, as part of preparing the requirement, be able to review the examples and agree that _when these examples are all satisfied then the feature is ready_. Being able to agree on this is essential for knowing when the feature can be shipped; without knowing this there will inevitably be discussion after implementation about extra things that the feature should (or maybe shouldn't) do.

## Wrap up

I hope this has shed some light on the benefits of BDD. It's good to keep this in your mind when managing BDD in your team.

 * Ensure there is discussion. No feature requirement should be exempt from discussion.
 * Focus on the WHAT, not the HOW. There could be many HOWs but only one WHAT. Leave the HOW up to the dev team.
 * Talk in a common domain language across **all** of your specifications and examples for consistency.

### Useful Links

* [Dave Farley on BDD](https://www.youtube.com/watch?v=gXh0iUt4TXA&list=PLiHKO3t8iHjRL2G6ngTJMsK19RGADJJXj)
* [Dave Farley on BDD (again)](https://www.youtube.com/watch?v=zYj70EsD7uI)


