---
layout: post
title:  "Don't Over Engineer: 3 tips for Start-up CTOs"
description: "Supporting a new company which is running on gut feel and passion is difficult. There is an amazing product lurking in there somewhere, but how do you find it? Here are 3 principles to guide you."
tags:
    - Software Development
    - CTO
    - Software Management
    - Agile
author: Richard Forshaw
---

I've been privileged to have been a CTO for a "Start-Up" for a number of years. Although I should clarify this is not quite true on a couple of points. Firstly, when you are CTO for a Start-Up you are not just a CTO; you are everything from a developer to a CTO, depending on the businesses needs and capabilities at any point in time. Sometimes I was a solo developer, sometimes I was an Engineering Manager, other times I was a DevOps Engineer, a Scrum Master and a Business Analyst. Every day requires a different hat.

The other half-truth is that the business probably isn't a Start-Up any more; it was a Start-Up for a year or so, but when you reach consistent revenue growth you have probably proven your product-market fit. Thus you are not really a Start-Up any more, but at the leadership level you still need to think like one.

What is definitely true though is during the whole time as a CTO I prioritised getting the right features out at the right time as fast as possible with whatever budget we had. This, to me, is one of the most central points in being a Start-Up CTO, and embodies typical 'Lean' thinking to the extreme, because if you don't get the right features out at the right time then it could spell the end of the business.

I was recently invited to have a chat with another "Start-Up CTO" and offer my advice. He reminded me of myself when I first started - constantly changing roles, constantly changing priorities, always being asked to prioritise every feature. In talking to him, it gave me a new perspective on the role and we had a very productive chat. Below are three things that came out of the conversation which I think are valuable to any software professional especially in a Start-Up/Scale-Up environment.

![Focus](./images/scrum-board-and-magnifying-glass.jpg)

### Focus on Value

The number one complaint of the CTO I was chatting with was the sheer number of features that he was regularly being asked to implement. Of course, he felt obliged to implement them all. When I dug further, I discovered another dimension which was not easy to see; while some of these features were for demos to 'trial' customers, some were really for 'show-and-tell' pitches for potential customers. This meant that many features were not even being used beyond a given deadline. Over time, this curse of un-used code compounded on itself, as code that was not being used was then being **fixed** in order to integrate with **new code which would also potentially never be used**!

I had my own version of this story; I was asked not long ago to start working on a new feature for the drivers at Instatruck, allowing the Instatruck Smart-Matching system to automatically match vehicles to jobs according to some additional truck features. I discussed with the management team and we came up with a set of new code features. This affected probably 10% of all vehicles and an increasing number of all daily job requests (some days maybe 30%). So it was worth the investment.

A few days later I was asked to add even more features to the feature set, but I was confused because these features had not been mentioned before. After some investigation, I found out that the additional features probably affected less than 1% of the vehicles in the system, and the drivers had only requested this specific behaviour a handful of times in the last few years.

This is a typical case of scope creep, where it is easy to make yourself feel more productive by adding extra bells and whistles onto a new feature. As a CTO, you need to have one foot in the business-side of the job, and so it was my duty to suggest that these extras bells were not worth pursuing.

My guidance to the other CTO was to understand that he had at least three types of 'feature customer'. Firstly, real customers who are paying real money. These customers should have the most time invested in new features, lest they are disappointed and go away (and stop paying). Second, 'trial' customers who are not paying but might be. They can probably put up with new features that are a little rough around the edges.

Finally there are 'customers' in demos and pitches. They are only evaluating a feature very briefly, and in some cases not even using it - the founder or the sales team could just be showing a concept to them. In this case your real customer is the sales team - what do they need to be able to complete a successful pitch? Maybe it is just some conceptual videos. Maybe it is a basic web-only implementation with some fake data. In these cases not only do you focus on where the value really lies (what the sales team needs to achieve), you also save time in not implementing a full feature which can then be used on the feeatures that really do need a full implementation.

![Complex gears](./images/luxury-clockwork-design.jpg)

### Don't Over-Engineer

Many years ago I was doing a coffee-consult for an interior designer who had recently done a fit-out for a number of meeting rooms in a new building. They wanted to find a way to get feedback on the utility of their rooms, and in the midsts of a wave of hot app success-stories, they thought that an app was a way to do this. They pitched me their vision of a geo-tracked app that would know which building and room you were in, and would connect to your meeting calendar as well as detect you entering and leaving one of their rooms, upon which it would prompt you with a set of feedback questions.

Could this app be built, they asked me, and how long would it take?

Now I am as excited by tech as the next guy and I figured this would be fantastic to build, but I had to ask a few questions first. How many rooms did they have? How big was their audience? How had they gathered their feedback so far? These questions were to gauge how effective this would be at solving their problem and come up with a back-of-the-envelope ROI on what would probably be quite an expensive thing to build.

In the end, I suggested that they buy some coloured ping-pong balls and plastic containers and equip each room with a sign instructing users to vote on if they think the room is good or not. This is essentially a \$100 experiment that can give you fast feedback on whether you should then spend \$100,000 on an app to do the same. I knew I was risking a client in suggesting this, but these are important things to know lest you end up with half an app, no budget and an angry client.

This is another aspect to 'value' - identifying the fastest way to determine if your idea (or feature) has legs, and if it should be pursued with real time and money. As early-stage CTOs we need to remember that we have a limited runway, and usually there are more features than will fit on that runway. Running simple experiments is essential to knowing which feaures are most likely to extend your runway, after all the worst mistake you can make is chosing features which eat up your runway and no-one uses over those which will be game-changers as soon as they are launched.

![Flexible Yoga](./images/yoga_sequence.png)

### Flexibility vs Stability

As the custodian of a team, you need to put it to its best use. Your team is your toolbox, and it is very adaptable, but adaptability comes at a price. The CTO I was talking to was suffering from an additional symptom of having too many features to deal with - they were coming in very quickly with the request that they were also the new number-one priority (which is of course what happened when the last set of features were requested).

This is a fact of life in a startup - the founders always want everything done and are reluctant to choose some features over others. But an incomplete feature is no good to a customer, so prioritising features needs to be balanced with completing features, and features can only be completed if the team is able to focus long enough to complete them.

As a CTO, you need to be the layer that balances these two things - be flexible enough to work on the things that are most important and be stable enough to finish the things you are working on. Nobody wants a bunch of half-finished features but you also don't want to be working on things that are no longer relevant.

One way to do this is by fixing a cadence for delivering work. If you are pivoting and experimenting quickly then this might be set at a week. At the start of the week, goals are set which can be achieved in that week. Within the week the team is left alone to get it done. Interruptions should only be for critical issues, and otherwise new features coming in should be parked in a backlog and prioritised in time for the start of the next 'fixed period'.

When we used this technique at Instatruck we had three levels:

 - a weekly team goal used to provide a cadence of features and internal prioritisations (usually to resolve dependencies)
 - a monthly business goal to agree on the priorities for the month
 - a quarterly strategy to identify any major re-focussing of the business
 
 This worked well, as monthly priorities were run against the previously-agreed quarterly-strategy to confirm they were in fact priorities, and the weekly release cadence was used to show progress to business stakeholders and get fast feedback.

### Round-Up

 - Value is key to getting a Start-Up off the ground, but features that are important one day may not be as important the next.
 - The value that you agree is important is also only valuable to the business if it gets to customers, so some stability is needed.
 - Not all of those customers are equal in your adoption funnel, so the investment you make in each feature may be different. Some may need a different approach altogether
 - Sometimes quick and dirty is OK, and even a non-technical solution is OK as long as it gives you important validation.

Hopefully these principles can help to filter & fund features in your business!

