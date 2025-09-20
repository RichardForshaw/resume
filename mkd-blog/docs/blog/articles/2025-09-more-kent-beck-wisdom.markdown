---
layout: post
title:  "More Kent Beck Wisdom"
description: "The ideas that Kent Beck laid down in his books were innovative when he wrote them, but there are good reasons to still think the same now. Here are 5 thoughts that inspired me again"
tags:
    - Software Development
    - XP
    - Agile
author: Richard Forshaw
---

I have had Kent Beck's 2015 talk on YouTube at the Lean IT Summit queued up for some time, and today I found myself on a plane flight from Sydney to Perth with hours to spare. Having skipped over this one a few times I decided it was time to watch it.

Titled ["Extreme Programming 20 Years Later"](https://www.youtube.com/watch?v=cGuTmOUdFbo),  I was expecting a presentation on the principles and processes of Extreme Programming, and how they had changed over the years. A kind of retrospective. Instead, it is a high-level timeline on Kent's journey through programming, consulting, TDD, JUnit and Extreme Programming through to his time at Facebook, but that doesn't prevent him from dropping a number of gems which I couldn't resist jotting down.

Part way throught his talk, he relays an anecdote about how he wrote most of the Extreme Programming book on a train from Zurich to Munich. Apparently it is a good stretch of railway for writing. Taking a leaf from Kent's book, while on the flight from Sydney to Perth I decided not to procrastinate and write this blog post with everything fresh in my mind. Hopefully it is a good stretch of air-way.

Without further ado, here are the parts of the video that jumped out to me.

![Extreme Programming Title](./images/ExtremeProgrammingTitle.png)

## The Inspiration for TDD

Kent explains that his father (also a programmer) would bring home books on programming which Kent would read. Being the 1970s, the books dealt with computers at the time which were largely tape-driven. One book that he read described the following process of writing software:

 1. Take an 'input' tape, and generate an 'output' tape containing the data that you expect your program to generate
 2. Do some programming
 3. Run the program and compare its 'output' tape to your desired 'output' tape
 4. Adjust and go to 2

This was the basic programming cycle, given the limitations of the equipment at the time. It was also a direct inspiration of TDD. As Kent tells it, it was simply an obvious way of programming. Let's convert it into TDD:

 1. Take your input to the system or function, and generate the output (i.e. a test) that you expect the new system/function to generate (or 'pass')
 2. Write your function
 3. Run the test and see if it passes
 4. Adjust and go to 2

Look familiar? Thus, from an existing discipline, was born TDD. It's amazing to me that the standard way of programming 50 years ago still contains valuable lessons in how to work effectively. Perhaps the 'old' is never really old.

#### TDD Benefits Recap

I think that too many programmers still run steps 1 and 3 in their heads, which is to their detriment. The benefits of writing the tests first that I have encountered include:

 - It forces you to think *in terms of your function or system interface*, i.e. the 'design'. When dealing at the unit/function level, TDD naturally lets the interface/design to the new function emerge from the perspective of its client. From a system level, it lets you express the interface in terms of user interactions.
 - It makes it easy to quickly scale your tests horizontally. I'm using the allegory here of horizontal (capacity) scaling vs. vertical (functionality) scaling. Many test frameworks these days allow for easy parameterization, and this is 10x faster than you performing yet another manual test on your code.
 - It naturally reveals when you are finished. If the new behaviour has a known scope, this should map to a finite number of tests. In the video, Kent reveals "I couldn't think of any more tests to write, so I knew I was done." This is something I have revisited often with junior developers: write the tests that you expect to pass and you will know what your progress is. If you have formulated 10 tests and there are 6 passing then your progress is very clear.

## TDD Makes You a Crafstman

Before TDD, it was typical, perhaps ubiquitous, for developers to write some code and then pass it over to a QA team to evaluate whether it was working or not. This was not only a separation of process and workflow, but also a separation of accountability. Working this way (and hopefully nobody reading this is working this way) meant that software developers were effectively stating that quality was not their problem.

How could this be? If a tradesman came to your house to repair or install something, would you expect them to walk away while a quality inspector decided if the work was suitable, then to call the tradesman back again? I hope not.
 
The book "The Pragmatic Programmer" is written around software development being a craft, and craftsmen own their own quality. By saying "I'm finished", you should also be saying "I have completed this task to the specification you wanted and I can prove it". This is a big deal, and Kent refers to this as a bit "Political Shift" in the industry.

Developers that don't own the quality of their work don't have a place on my team.

![Never stop learning](./images/never-stop-learning.jpg)

## Always Be Learning

Three weeks into joining Facebook, Kent admits that he was out of his depth. As he puts it: "Either they were morons, or I was. Turns out I was." At this point he "decided to forget almost everything I knew about software development" and started learning again.

This is a big lesson. I am currently reading a well-timed chapter in "Ego Is The Enemy" about how we should always be students. A passage I highlighted is
 
 > The pretense of knowledge is our most dangerous vice, because it prevents us from getting any better.
  
To his great credit, in this moment Kent shows how he was willing to become the student again. After introducing his own paradigm-shifts in TDD and XP, he was able to clearly see another shift that was happening to him, and embrace it as an opportunity.

We should all be like this. There is always something to be learning, and there is always a teacher to find.

## The Staring Dog Problem

This one was new to me. The staring dog problem is that when you point out something to your dog, it will focus on your finger rather than what your finger is pointing at. But how does this relate to Software Engineering?

Kent tends to write his books (on my sample size of 2) using a values/principles/practices model.

  - The **Values** are the key qualitative aspects of your work that are "inherently good". They are your foundations; maximising them brings great rewards. An XP example is **Feedback**: feedback is essential in guiding you from an initial solution to a good solution
  - The **Principles** are rules or guidewires that you can apply to your work to guide you towards maximising your values. An XP example is **Baby Steps**: Doing one small improvement at a time is a way to get quick feedback about the progress to your solution.
  - The **Practices** are the daily habits or processes you can implement to have a measured impact. An XP example is **writing a single test first**:  this is a single Baby Step that you can do every time you code.

I have recently embraced this triad-model of drilling down in my own development when I started writing things in terms of Tasks, Impacts and Progress; I look for a positive impact on the team or system, then I look for the measurements that can show an improvement in these impacts, then I look for tasks we can implement that can improve the measurements.

It is my new way of ensuring my work has purpose, and even if you are staring at the master's finger, it can still lead you to big impacts.

![A data graph](./images/data.jpg)

## "It Turns Out" that Data is Important

Measuring your impact is important. Kent acknowledges that another value he had to learn at Facebook was to always be informed by data. Data shows insights, reveals problems and shows progress (as described above).

I attended a talk given by Atlassian engineers which focussed on exactly this; if the team wanted to remove Tech Debt in some way, they were asked to provide a measure of their progress and use it to demonstrate the improvement while they were completing the task.

This inspired me to start thinking in the Task/Impact/Progress format above, as not only should I be demonstrating progress along improving impact, I can also be demonstrating _progress of implementation_.

Kent then reveals the "most exciting words an engineer can say", and it is exacly the gathering of data that allows it to be said:

**"It turns out that..."**

 - _It turns out that_ smaller issue sizes do speed up development
 - _It turns out that_ our real bottlneck is waiting for code reviews
 - _It turns out that_ introducing WIP limits has halved our feature development time

If you can begin a phrase with "it turns out that...", it means that you have hypothesized, experimented and analyzed. And then, you are an engineer, my friend.

## Epilogue: Naming is Still Important

As part of his "Lessons Learned" of what he would do differently, Kent higlighted the naming of "Extreme Programming" itself. He admits he would have chosen another name because there were a number of assumptions and inferences that could be made with a word such as "Extreme". Curiously enough, this is one reason why I didn't explore it when I first heard it in the early 2000s.

I knew there were shifts happening in the industry and I wanted to get on board. Scrum was a thing, Iterative Development was a thing, Unit Testing was a thing, and there was also something called Extreme Programming. I didn't look into it too hard because, as part of a professional team, I thought that something with a name like that would be a hard sell to my team leader.

Little did I know that the concepts of all the other things I was looking into were all wrapped up in Extreme Programming. So yes, names do matter. Perhaps with a different name I would have jumped on board much, much earlier.

So here is your chance to start exploring it!

