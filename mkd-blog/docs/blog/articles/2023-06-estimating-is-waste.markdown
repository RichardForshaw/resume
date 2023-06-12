---
layout: post
title:  "Estimating is Waste"
description: "I previously thought that even though agile-based priorities hold more value than estimating, there was still value in estimating. Now I'm not so sure."
tags:
    - Software Development
    - Agile
author: Richard Forshaw
---

Many years ago I wrote my first software blog post: [Backlog Priorities](./2018-11-28-backlog-priorities.markdown). It was about estimating. Looking back you can tell it was my first attempt; after nearly 2 years of regular writing I think I have improved. But what has also changed is my opinion on that topic.

In that article, I started down the path of moving away from estimating, and instead focussing on prioritising tasks and delivering value over trying to identify how long things will take. However I hung on to estimating in order to throw some rope to the people with the purse strings. After all, you need to know how much runway you have, right?

Recently however, I have started to climb the ladder of #NoEstimates. In reading more about Lean, and watching some critical but reasoned videos, I am moving to a new opinion: Estimating is wasteful.

![recycling bins](./images/recycling-bins.jpg)

## Lean and Waste

This year I [interviewed Nick Jenkins](./2023-03-nick-jenkins-lean-interview.markdown), and we talked about Lean. We talked about the concept of Value, but we skipped over the concept of Waste, which perhaps still needs to be spelled out. As quoted in that post:

 > the definition [of Value] is basically that it's what a customer will pay for

From this it should be plain to see that Waste is *anything that the customer shouldn't pay for*. In other words; anything that does not provide the customer with value.

Now this is pretty extreme. You could say that having a fancy office or free cupcakes doesn't provide the customer with value. But some of these things can be indirectly linked to the stability and productivity of your workforce, which does add customer value. After all if your workforce left to work for your competitor who has those things then how would you deliver that value?

But what you can put into the basket of Waste (in sticking with the theme of being extreme) is estimating. And meetings. And over-complicated work management tools (there's no need to name names here).

![Serving Coffee](./images/coffee.jpg)

## The Lean Cafe

Think about a cafe. The value of the cafe is producing coffee, or producing food and snacks, and the more efficiently you can do those things, the more value you produce, which directly affects how much money the cafe makes.

One thing that doesn't happen when a customer orders 2 lattes and a french toast is that a manager pulls the team into a meeting room and they perform some estimates on how long they think it will take. They just start. Imagine the bewilderment on the customer's face if this were to happen, and then to make things worse the cafe charges them for the meeting time.

I do of course realise this is an over-simplification, but sometimes you need a simple analogy. Your software team isn't like a cafe, because making coffee and french toast isn't a complex problem. But the heart of the analogy still stands: the highest value-adding activity that the cafe can do is actually make the coffee.

## Habits and Rituals

The two videos I watched recently which began to swing me are Gary Strahan's ["Development That Pays"](https://www.youtube.com/playlist?list=PLngnoZX8cAn-cLyBLerru-kROqXN3wrkU) series and Allen Holub's [#NoEstimates presentation](https://www.youtube.com/watch?v=QVBlnCTu9Ms&t=1889s). They both essentially agree on the same things:

 * Estimating is a wasteful activity, because it adds no value to the customer
 * Estimates are also damaging because they are nearly always wrong and consume valuable time to create
 * Estimates are unfortunately deeply ingrained in our work rituals

![Elephant in room](./images/elephant-in-room.jpg)

Whenever we discuss a new task or feature, someone in the room instinctively asks "how long will it take". Both Gary and Allen then reveal the elephant in the room: once a developer answers that question, in management's mind it becomes a commitment. This of course causes anxiety for the developer because they know that this is happening, but (and I have tried this) even if the estimate is prefixed with a wordy and pleading disclaimer, once that time is elapsed they know that they will be stigmatized as 'being late'.

Allen traces this back to an old assembly-line notion of 'scientific management', which included a practice of placing a 'Time Manager' next to the worker's station. This manager would literally hold a stopwatch and measure how long the worker took to perform their task. If it was not up to expectation, they would escalate their findings to the 'Time Boss', who would then prescribe what needed to change at that station in order to improve performance.

Sounds crazy right? But underneath, is this still essentially what is happening today?

The most baffling part of this story is that there was an *entire job* dedicated to measuring an reporting at its most basic level, and that all the autonomy was being stolen from the person actually doing the work. Compare this with the story of the [65,000 improvements a year delivered by VistaPrint](./2023-03-nick-jenkins-lean-interview.markdown#improve-and-empower).

## If No Estimates Then What?

The videos linked to above both build on the work of [Vasco Duarte](https://www.youtube.com/watch?v=MhbT7EvYN0c), who applied empirical analysis to software delivery. The core message of all these messages is: Don't Estimate, but Do Project.

At the risk of being too brief: If you measure your story-point delivery over a small number of sprints, you can project the final completion with much better accuracy than any prior efforts to estimate.

This came as a pleasant surprise to me because I was planning on writing a post about [another misconception about Scrum](./2022-12-Scrum-Misconceptions.md): Story Points and Velocity. It took me a while to realise, but it is crucial to separate story-sizes from time. This is a difficult thing to do because of how we are ritualised to always think about time, but one of the best ways to estimate future work is to calculate your story-point velocity.

Until, that is, Vasco Duarte revealed that *simply counting the number of stories is just as good as tracking the story points*.

It took me a little time to comprehend this, but this comes back to Lean Development and detecting waste: if stories-per-sprint is just as good as story-points-per-sprint, then *even estimating story points is wasteful*.

![Blow your mind](./images/mind_blown.jpg)

## What Counts: Counting

The key thing is to track your stories, wait a few sprints (which will require some new discipline), and project. But the Gary Strahan interpretation goes a little further; he rightfully says that there are two valuable activities that can be preserved from the estimation meetings that we are trying to move away from:

 * Discussion and understanding; and
 * Decomposition

Stories and features need to be discussed and understood. This obviously helps developers to comprehend the nature of the requirements and discover complexities. It will also move the stories or features much closer to the "Ready" state and require less interruptions during the sprint. But we should also recognise that a simpler story is more likely to be achieved that a complex one.

Smaller stories also allow us to deliver quicker and achieve another central tenet of Agile: feedback and adjustment. Decomposing a complex story and prioritising its components may still reveal those which are much more valuable than the others. Surely the most wasteful thing is to find out that you have spent some of your budget on something that none of your customers wanted to use.

So in the style of the old agile manifesto, I think this is what the #NoEstimates movement is trying to teach:

 * Prefer projections over estimates
 * Prefer story understanding over story points
 * Prefer prioritizing value over scrutinising budgets

Vasco, Gary and Allen are all preaching moving away from estimates. Now that I understand, I think that I'm with them.

