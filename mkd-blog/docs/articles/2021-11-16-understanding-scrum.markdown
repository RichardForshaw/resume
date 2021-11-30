---
layout: post
title:  "Re-Learning Scrum"
revision_date:   2021-11-16
tags: Scrum Agile
author: Richard Forshaw
---

![alt text](images/classroom.jpg "Re-Learning Scrum")

I have a confession to make. Over 20 years into my software career I didn't actually know what Scrum really was and why it was good.

While I'm confessing things, until a few years ago, I also didn't really know what made a "real" unit test. Or what the key philosophy behind functional programming was. I just knew some essentials about these topics, and knew some good arguments to support them: Scrum and agile require prioritising the frequent delivery of small functional iterations; unit tests should be small and fast and have a high coverage; functional programming should deal only with inputs and outputs and have no side-effects. So I practiced good software delivery habits, I wrote lots of unit tests and I tried to write 'good functions'.

Why am I confessing this? Because I think that many software professionals are in a similar position. Looking back, I think many people I worked with were in the same boat. We often discussed these topics, we talked about the books and authors, and we did the things that we thought the books were talking about, but we mostly hadn't actually read the books or really understood the concepts. The best case was that we had been in enough discussions and read enough snippets from Hacker News that we knew about the key concepts and how to argue positively about them. We walked the walk, and I can vouch that we achieved some great things, but we didn't really know much about the path on which we trod.

It's OK, you can admit it too: you know enough about why Scrum and Agile are better than waterfall and enough about how to 'do' Scrum that you can go through the working day extolling the fact that you are 'doing' Scrum. I don't deny that it is good to know these things, but the key question is: why? Why do we do the scrum activities? What are the key benefits? Try to answer those questions without just saying "it's better than doing waterfall". For all you know you are just doing ['waterfall wrapped up as agile.'](https://www.mountaingoatsoftware.com/blog/an-iterative-waterfall-isnt-agile)

I remember going through the Scrum motions on a project 10 years ago. I was brought in as an Engineering Manager for a small R&D company. I guess you could say they were doing 'automotive research'. I introduced Scrum. We did the 'scrum things'; we had a backlog and we did the daily standup. One day one of the team members said 'why do we need to stand up for this meeting?'. I answered with one of the rote phrases I had read and heard before: "so that the meeting doesn't last long". But as I heard myself say those words I had a doubt that I really knew why, or if the person who asked had a valid point or not. And with every year that passed and every question raised, I had the same feeling.

## Back To School

I couple of years ago I went to a conference and met a couple of agile practitioners with whom I had some deep discussions. We shared stories and agreed on many things. But one thing I noticed was they were one level above me in answering questions and explaining concepts. The kind of knowledge which reveals that you not only know the 'what' of a subject, you also know the 'why' and can use that 'why' to explain many more 'whats'. At this point I felt inspired to increase the depth of my knowledge. After all, I believe that to really be able to benefit from a topic and expand it meaningfully you have to understand it deeply, and I think that instead many of us learn new things by osmosis because of a lack of time.

I decided to read a Scrum book - properly this time, with a highlighter and a notepad. I now know I should have done this a long time ago. The book was ["The SCRUM Fieldbook"](https://www.goodreads.com/book/show/43582738-the-scrum-fieldbook) by JJ Sutherland, and I summarise my new understandings below.

## Scrum Recap

The readers of this article probably know the basics of Scrum, and use it to deliver increments of a software product. You know that you start of with a **product backlog** which contains all the work needed to be delivered. You then pick some of this work in conjunction with the **Product Owner** to work on in the next **sprint**. You have a daily **stand-up**, and probably if you look around your office most teams are having a standup at the same time. You answer three questions in the daily scrum: What did I do yesterday, what am I doing today and am I blocked on anything. This happens every day and with a bit of luck you complete your sprint on time and demo it to the product owner and stakeholders. You then hold a retrospective and talk about what went well and what didn't.

Does this sound right? That Scrum is mainly about following these 'rituals' which are designed to help you deliver the features on time and maybe over time you will learn a few things and go faster. So therefore scrum must be a software delivery/project management tool. It's just designed to be incremental and avoid a 'big bang', right?


## The Problems

JJ Sutherland's book dives into the problem that we have all heard before: that delivering a complex software system does not work in the traditional way in which products were designed up-front and then planned to be delivered by a certain date. As he mentions in the book, a Standish report from 2015 stated that **40% of projects** that used a 'waterfall' model (of up-front design and scheduled delivery) resulted in failure, which was defined as being either late, over budget or not delivering to expectations. That is a scary figure. It means that if you set out to deliver a software project in that way, it was almost a coin-flip that you would fail.

Why does this happen? What are the root causes of this delay or failure? The book focuses on the following:

 - Unknown Problem Complexity
 - Decision Latency
 - Inspection with inaction

### Problem Complexity

The thing that these failed projects have in common is that they are _large and complex_. The other attribute that they posess which people often forget is that they are uncertain, and we constantly fool ourselved into thinking that large and complex problems can be predicted up-front: i.e. the 'waterfall' strategy. The key thing to understand is to recognise the difference between **complicated** and **complex** problems, which the SCRUM Fieldbook discusses through reference to the Cynefin framework. Complicated problems are those which are difficult to solve but the methodology is known; you basically know what you have to do. This is the domain of the expert: Solving simultaneous equations could be classified as complicated to high-school students, because once they are taught the process then it becomes knowable, you just have to put the work into solving it. Bug-fixing is usually a complicated process - you know what the problem is and you have tools to drill down and solve it, so usually you are able to find and fix the problem using your learned skills.

Complex problems are where the idea of 'unknown unknowns' comes into play: you don't really know where to start; you don't know what you already know (which would allow it to become a complicated problem); and you don't know what you don't know or can't solve. You have to learn as you go along. I recently spent a lot of time trying to 'solve' the Travelling Salesman problem within a finite time. There were some things I knew (such as the exponential nature of the problem), but some that I didn't (such as the presence of graph-simplification tools and strategies), and more importantly I didn't know whether they would help. The key insight in the SCRUM Fieldbook is that the solutions to complex problems are emergent - you simply have to try something and see what happens. I had to try many things and research many mathematical tools before even having a chance of quickly solving 20- or even 30-node TSP problems (for info: 20-nodes equates to over a quadrillion possible paths).

### Decision Latency

A key problem presented in the book is 'Decision Latency'. This rang a huge chord with me and I'm sure it will with others. How long do you have to wait to get a decision on something that you needed? During projects I was involved in, I recall having to wait probably no more than a couple of weeks to get a decision and they mostly involved either hardware or resources. But perhaps I was lucky - the book mentions decisions taking up to six weeks. You might say that those type of decisions probably aren't trivial, and that is probably true - those type of decisions are probably outliers. But the Standish report data implies that in places where this kind of latency exists, even the trivial decisions are impacted because of the organisational structures at work. The report goes on to say that projects with "poor" decision latency are three times more likely to fail than those with "good" latency. Which seems obvious when you think about it.

The book "Developing Products In Half The Time", written independently of Scrum, targets the same thing. "Rapid development projects must make many decisions in a compressed time period" it says. Furthermore, upper-management usually position themselves within this decision-making path because they believe they are best placed to make them. This is however a delusion: the managers mis-attribute their ability to make the decision based on their analysis of the data with the total time taken to deliver the decision from when the problem is identified. In other words, these managers are typically good at making the decision, but the organisation is not good at preparing the manager to make it and is also not good at identifying exactly how much of the project's time has been spent on it.

### Inspection with Inaction

Many people walk around their organisations knowing that there is something wrong within the project. I was often one of them; I would know that doing something a certain way would be hurting performance, but as a junior (and sometimes senior) developer I did not know what to do about it, so the extent of my action was to join in with the complaints that my team-mates were making.

This is because 'inspection' is usually not a problem, but it is only enabled or present at the individual level; team members will have a good idea about what is slowing them down, but there may be a hidden culture which prevents this from being revealed or reported. Or perhaps if something is revealed by a team member, the organisational reaction will turn the potential solution into a decision, in which case it will be subject to the decision latency problem described above.

The SCRUM Fieldbook refers to this behaviour in one section called "Rules Should Fight For Their Lives", which requires the candour and bravery from the team to question things that they feel are hindering them. Software developers often talk about code-smell, but the rules and processes present in a company can also be evidence of organisation-smell. These are ways of working that have been around for so long that no-one really knows why they are there and people generally assume that they are still relevant. This can also be absence of process - the group collective can often self-organise into an unwritten way of working inefficiently that becomes a 'silent rule' which nobody wants to break.

## Summary

These are the three key problems that I took from reading the SCRUM Fieldbook as the biggest causes of the failure rates mentioned above. Hopefully you can see how these issues can map to the three definitions of project failure: Misunderstanding of problem complexity lead to delivering the wrong thing, and decision latency and stagnant processes both lead to time and budget problems. So how does Scrum deal with these? Stay tuned for the next part!


