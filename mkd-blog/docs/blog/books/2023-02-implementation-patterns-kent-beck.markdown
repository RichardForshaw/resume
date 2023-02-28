---
layout: post
title:  "Implementation Patterns (Kent Beck)"
description: "Kent Beck's 2008 book tries to examine what makes great code, what patterns are behind Object-Oriented constructs and how to make choices that will benefit the longevity of your software."
tags:
    - Books
author: Richard Forshaw
---

Kent Beck is a bit of a legend in programming circles. The creator of XP (and Author of "Extreme Programming Explained") and JUnit, I was able to see him speak and watch his mind work at a conference in YOW Singapore where he delivered his ["Explore/Expand/Extract"](https://medium.com/@kentbeck_7670/fast-slow-in-3x-explore-expand-extract-6d4c94a7539) talk.

I had "Implementation Patterns" on my bookshelf and decided to read it to see what messages it had which may still be relevant today (it was written in 2008). There are definitely things in there still worth knowing, but a few things that maybe aren't.

![Implementation Patterns](./images/ImplementationPatternsBeck.jpg)

## Warning: Java

The book is presented from the perspective of Java, which means we are in for a ride of Classes, Interfaces and all things Object-Oriented. I admit I have kind of moved on from OO - I was a C++ developer for about 8 years, and when I moved to Python I tried to shake the shackles of OO-programming. Despite Java still being so popular, I think OO should be used wisely in certain contexts and I am now in the camp of 'use it when it's needed'.

If you are not programming in Java, there is still enough in this book to be relevant to the OO language that you are using. However if you are not using OO, you will probably struggle to find relevant information in this book. It is there, it is just wrapped up in such a deep OO-context that it is often difficult to extract.

If you are interested in things that might be relevant across programming-paradigms, check out my [post on his important insights](../articles/2023-02-3-kent-beck-insights.markdown).

## The Great Things

The opening few chapters (mainly chapters 3 and 4) are recommended reading for any serious programmer; that is those who want to become great and not just good. Everything I read in these chapters triggered a relevant memory from a project somewhere, or discussions held with team-mates. From code communication to the cost of code and through all the programming principles he lays out, all are still relevant today in some form, no-matter what your language of choice.

The other great part of this book for me was the deep-dive into Collections. Pretty much every popular programming language deals with collections in some form, but in my experience they are often just seen as tools from a functionality perspective and their specific use-cases and performance side-effects when dealing with very large data are rarely considered. Beck dives into this and presents information that I think every programmer should know about when to use and when not to use each type. This topic is worth the pages that he spends on it.

## The Good Things

Beck's explanation of classes is worth reading for beginner- or intermediate-level developers working in OO-languages, both as gaining a better understanding of the concepts behind classes and encapsulation and then understanding why you hear all this advice over choosing composition over inheritance and such like. Beck also spends a little time on often-discussed issues such as library classes and getters vs setters.

The other chapter worth reading is that on Frameworks, but I only suggest reading it if you are maintaining a framework (either public or private) or you are working high-level on a large OO system. There are many useful tid-bits from Beck's time working on JUnit but they are quite advanced.

## The Rest

I found the rest of the book to be a bit hit-and-miss. Perhaps this is because I am not a Java programmer and no longer an OO-programmer, but despite that it felt a bit dated and the useful information came up sporadically. It may still be worth dipping into this book just to look at specific ideas or OO concepts.

The book was also a struggle to read sometimes, and I expect it would be more so for new programmers. Despite having some good examples, I sometimes found it difficult to extract the critical meanings. This may find it hard for some readers to discover the real gems contained within.
