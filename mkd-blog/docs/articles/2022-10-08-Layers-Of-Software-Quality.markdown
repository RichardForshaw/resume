---
layout: post
title:  "The Multiple Layers of Software Quality"
description: "I had a discussion recently where I was asked: 'How do you go about ensuring quality in your software?' I used to think this was a simple question, but that was when I was young and I only looked at the world in a certain way. After several years of experience I am uncovering and understanding more aspects of quality."
revision_date: "2022-10-08"
tags:
  - Software Quality
author: Richard Forshaw
---

![Four Diamonds](images/BigDiamonds.jpg)

I had a discussion recently where I was asked: "How do you go about ensuring quality in your software?" I used to think this was a simple question, but that was when I was young and I only looked at the world in a certain way. After several years of experience I am uncovering and understanding more aspects of quality.

The funny thing is that the dictionary definition of quality does not cover any of these aspects. Instead it defines quality as "a standard something as measured against other similar things", or "a degree of excellence of a thing" or even "an attribute or characteristic possessed by someone or something". But these definitions are not a good fit for software, and are something we need to move away from.

### What is it then?

As a junior developer I remember being in a Software Quality meeting, and being shown an appropriate definition of quality - imagine you go and eat at McDonald's. You order a Big Mac. then you go to another store and have a Big Mac. Then you go to another city, or another country and have one. And they are all the same.

![Big Macs](images/bigmacs.jpg)

That is the quality definition they were putting across - that no matter where you are, what you expect is what you get. It is always the same. In the case of McDonald's, a Big Mac is always the same Big Mac. It doesn't matter if you are in Kansas or Kiev, London or Lesotho, it is the same, and it meets your expectation as a consumer.

The key phrase here for software is "what you expect is what you get". What goes in (expectations) matches what comes out (functionality). Wikipedia describes exactly this, and goes a little further:

> Software functional quality reflects how well it complies with or conforms to a given design, based on functional requirements or specifications. That attribute can also be described as the fitness for purpose of a piece of software or how it compares to competitors in the marketplace as a worthwhile product. It is the degree to which the correct software was produced.

### Product Level Quality

The level we are probably most familiar with is the Product level. This is what software teams are evaluated against feature after feature, sprint after sprint. Does what you have delivered match what was asked for?

When you finish a sprint and show your stakeholders, it is the time for them to tell you if you have understood them correctly. But a seasoned Scrum Master knows this is not the only thing to inspect; it is also the case that the stakeholders should have explained themselves well! If you run a Scrum team, the frequency that work is sent back is a key metric into understanding how well your stories are both described and understood before you start working on them.

In Jeff Sutherland's book ['SCRUM: The Art of Doing Twice the Work in Half the Time'](https://www.goodreads.com/book/show/19288230-scrum), I read, possibly for the first time, the concept of a "Definition of Ready". It is interesting that this is a concept that I talked about sometimes within a team, but not as much as hearing about a "Definition of Done". The closest I came to a process that fed directly into a "Definition of Ready" was when I started taking part in the [BDD Example Mapping process](https://cucumber.io/blog/bdd/example-mapping-introduction/), which I loved. One key think about an Example Mapping session is that you must come out of the meeting with _work that is ready to be started_. If you can't do this then something has gone wrong.

### Technical Level Quality

I am from the old days of programmers, and I remember when software 'quality' was measured in [SLOC, Cohesion v Coupling and Cyclomatic Complexity](https://en.wikipedia.org/wiki/Software_metric) (the last one I was actually quite fond of). Thanks to advances in programming language design and the DevOps movement, those metrics are unheard of now, and instead we are running on Deployment Rates, Change Lead Time and MTTR.

Real studies have shown that these metrics are a high predictor of team performance and can be used to attribute both a high level of technical quality and a high level of process quality. That process quality may be a high level of automated processes which allow more features to be deployed, or a high level of team maturity leading to minimal rework. The recent maturity of DevOps means that these metrics are easy to gather and analyse, and easy to identify improvements that need to be made to improve these metrics.

![Vegetables In The Market](images/MarketVegetables.jpg)

### Market Level Quality

Having delved deeply into Scrum recently, which is a derivative of Agile, it holds the concept of value highly. This is yet another aspect of quality, and I am glad that the Wikipedia article mentions it, noting "how it compares to competitors in the marketplace as a worthwhile product". Value is the market's view of quality - how well does this product help me achieve my goals.

A Product Owner in a scrum team should ideally be a customer, but is often a proxy. Even if the PO is an experienced proxy, they cannot fully represent a real customer, and even if the PO is a real customer, they cannot fully represent the entire market. That is why your product's quality in the market still needs to be measured. How often are features being used? Are they being used but abandoned? Did the customer enjoy using them?

Some of these metrics are easy to gather and some are hard, but they cannot 100% be replaced by a PO. As with many things which are part of a multiple-layered whole, they vary in difficulty but also in value; this type of quality may be difficult to measure but it may prove to be the difference between an iPhone and a Blackberry, or a Facebook and a Friendster.

### Feedback

These are three types of quality that I have identified, and they need to be made use of in order to maintain an advantage in the market. They each refer to a different aspect or level in the company and they have a different measurability and feedback frequency, but they can be all harnessed to improve your product; Product-level can be likened to software verification (is this the right product?), Market-level can be likened to software validation (is the product right?), and Technical-level to your overall efficiency, reliability and performance.

So next time you are asked "how do you measure your quality", think about your own context and the context of the person asking the question, and find out which aspect is the right one, but don't neglect the others.
