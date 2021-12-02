---
layout: post
title:  "Re-Learning Scrum Part 2: Scrum's Answers"
revision_date:   2021-12-02
tags: Scrum Agile
author: Richard Forshaw
---

![alt text](images/teacher.jpg "Re-Learning Scrum")

Welcome back! We have seen in the [previous article](2021-11-16-understanding-scrum) that three big problems causing poor performance are:
 * not understanding the nature of complex problems,
 * decision latency, and
 * a lack of action in finding and executing efficiency improvements.

I believe that these issues represent many if not most of the root causes of the 40% of failed complex projects. And these are the things which Scrum attacks.

## Complexity

The solution to the complexity problem is probably the one that readers will be most familiar with: delivering iteratively. But it is not as simple as it sounds - the real key is to creating fast feedback loops. There are two reasons why this is a solution to the complexity problem - one is the communication of a complex requirement and the other is understanding if that requirement is correct. There are many feedback loops built into Scrum, and two of them are related directly to these points: feedback from the stakeholders and feedback from the market.

Why do you need stakeholder feedback? If you have ever worked on a complex problem before, you will know that communication is difficult. Communication can even be difficult with less complex problems! But certainly with complex ones. There are many nuances on both sides of the stakeholder-developer relationship:

 * The stakeholder has a picture in their mind on how a feature should work but it is not always communicated fully: assumptions may be made that the developer is not aware of, concepts may be confused or entangled, and details at the micro level may be left out.
 * The developer has a deep understanding of the system, and the complex pathways through it: limitations in the system may not be known to the stakeholder, multiple steps of a sequence may be required in a certain order, and (my favourite) there are usually multiple failure paths for every success path that are often overlooked.

Scrum sprints are made short to provide regular opportunities for feedback to address these problems. Some of them should be ironed out at the start (refer to [BDD Example Mapping](https://cucumber.io/blog/bdd/example-mapping-introduction/), of my favourite things which I will write on another time), and others should become apparent and dealt with during the sprint (see below), but there will still be gaps in the knowledge that get through. This is where the **Sprint Review** comes in: to break the habit of misunderstood or incomplete requirements. Not only is it is very demoralising to a developer to work through a feature only to find out after releasing it that it is not "what the customer meant", the best time for a developer to adjust something is when they are still (or just fresh from) working on it.

Feedback from the market is more concerned with emergent product design. Ensuring that the software is always releaseable means that feedback can be gathered from the Market faster, enabling the Product Owner to make faster decisions about the product. As the SCRUM Guide says: "That's what Scrum is: a series of small experiments in short periods of time to find a solution to a complex problem." Move, measure, adjust.

This is primarily one of the jobs of the **Product Owner** - they are responsible for product clarity and feature priority: product clarity is the ultimate in fast feedback - if a developer has a question during a sprint then they can ask the Product Owner. Feature priority is a major outcome of the Sprint Review: the feedback from the review of the completed features should result in concrete data from real customers (or their representatives) about what they really want, not what they say they want. After all this is an important distinction and critical in delivering the value that your customer need. As the SCRUM Fieldbook says: "If you have to wait six months to find out if your guess is right, well, you are planning with hope instead of data."

## Decision Latency

Scrum tackles the decision latency problem in two ways:

 - Decentralising decision-making
 - Including a key decision-maker in the team (the **Product Owner**)

As alluded to above, addressing decision latency is at the core of the **Product Owner** role (i.e. being present in the team to provide fast feedback) and also the concept of **small self-organising teams**. The aim of this is to make decisions _locally_ and _quickly_. Teams are classified as 'self-organising' because the teams are large enough to handle the complexity of the problem but small enough to not produce complex communication overheads, and most importantly are empowered to actually _make their own decisions_. Part of this empowerment must come from management buy-in and trust, but part also comes from the role of the Product Owner.

![alt text](images/AllenCurve.jpg "The Allen Curve")

Is there evidence for this? The book "Delivering Product In Half The Time" refers to the ['Allen Curve'](https://en.wikipedia.org/wiki/Allen_curve), which has been re-gaining some popularity recently. Documented in the 1970s, it measured the frequency of communication between individuals in organisations together with their physical distance from each other. It remarkably shows a 'half-life'-type relationship of communication over distance, with frequency 'bottoming-out' at around 20m, meaning that at 20m, 200m or 2km the level of communication was about the same. Conversely, the top 50% of all communication happens within about 5 meters. This is about the size of an office that can comfortably fit about 6 or 7 people.

Decision Latency is also affected by the feedback loops described above - it is easy to understand how regular feedback from the stakeholders and frequent releases allowing for timely measurement from the market provide the information allowing the Product Owner to make their decisions, and easy access to the Product Owner by the developers enables this information to be fed into the product as quickly as possible.

# Inspection with Action

Overlapping with these is the solution to inspection and inaction, or rather turning inspection into action. Identifying problems and acting to remove them is key to increasing the long-term velocity of a scrum team. Much like how the role of the Product Owner is to enable local and fast decision making, the role of the **Scrum Master** is provided to facilitate frequently inspecting sprint progress and team velocity and to act to remove the barriers to going faster.

When I was leading software teams, I tried to focus on making sure that the developers spent almost all of their time actually developing, and not concerned with too many other things. I had been a developer for a number of years and I was aware of the mental overheads in switching between writing code and dealing with problems that arose, and I wished that I didn't have to deal with those problems. The best feedback I ever got from a team member was that whenever he wanted to raise an issue in the **Daily Scrum**, he told me he was confident that I was probably already aware of it and that soon it would be dealt with.

This is part of what a **Scrum Master** does: keep on top of the issues and solve them as quickly as possible. Some of this comes down to localised decision making, whereas other problems will need to be solved by the developers themselves (enter DevOps) and should be scheduled into subsequent sprints. Any problems still remaining need to be escalated independently of the team and dealt with elsewhere in the organisation. But they all need someone to focus on them. The **Scrum Master**'s other job is to force these problem to get solved: if it's a Product issue, get the Product Owner to fix it. If its a tech issue, get the team to put it into the next backlog. If its outside the team, keep knocking on doors until it's fixed. The **Scrum Master** is in part the aggregation of that 10% of developers' time that is wasted on solving non-tech problems rolled into one focussed role.

## Summary:

It is a but difficult to describe what Scrum **is**. The Scrum Handbook says that "Scrum is a lightweight framework that helps people, teams and organisations generate value through adaptive solutions for complex problems." The Scrum Guide says it is a framework for generating value and generating it quickly. It's probably easier to understand what Scrum **does**. It helps organisations and teams tackle complex problems and evolve the solution quickly.

We can also safely say that Scrum is not a Project Management tool, and the faster this is understood the better. You will notice that there is nothing in the above descriptions about delivering features on time or in budget or meeting deadlines. There is nothing in there about managing a project. There is nothing about schedules. In fact if you look further, the three scrum pillars are Transparency, Inspection and Adaptation. Not Delivery, Efficiency or Management. I think this is one of the hardest things for organisations to understand.

In the words of the SCRUM Fieldbook: "Scrum is set up to reveal the issue that are slowing you down". It's then up to you to fix them. The types of problems it was designed to tackle don't have a development playbook - you have to write the playbook yourself. All those diagrams you have seen with the little arrow-cycles are there for a reason: inspect your progress or experiment results, deduce any required changes (to both your processes and your product) and implement them. The 'rituals' or 'ceremonies' as they are often referred to are there to **reveal** current problems in your processes, which in turn is where the Scrum values of Openness, Respect and Courage come into play: the problems in your processes cannot be revealed without openness and courage for raising issues, and respect for your teammates who are raising them. The Scrum roles and rituals are most simply there as built-in mechanisms to provide regular opportunities for this to happen. I intend to dive into these in more detail another time, but I think you can see with this diagram how well they overlap.

![alt text](images/ScrumWheel.png "Scrum Answers to the 3 problems")

## Should you use Scrum?

Good question. I think in most cases it is worth trying. It is possible that you already have a open and robust iterative culture which embodies the benefits listed above in your own ways. But sometimes you only think you do. Are you measuring your product's market acceptance, or are you just following a pre-planned sequence? Are you adjusting your work priority based on market and stakeholder feedback, or have you just cut your plan up into stages? Do you measure and inspect the time-to-market of your features, or do you assume that becasue you were fast last year you must still be fast this year now that your product is larger and more complex? Remember that Scrum is there to help you answer these questions, not to provide solutions for them - that is up to you.

Software projects are the obvious candidate for using Scrum. Even small softwrae applications generally carry complexity because they try to anticipate and automate human behaviour and decision making. The fast development time and reducing barriers to entry of software systems have also bred an increasing entrepreneurial attitude to software products which means that software is produced on the back of multiple market assumptions, the most extreme of which is simply 'will anyone pay for this?' This plays directly into the hands of Scrum's mini-experiment foundations.

Should you use Scrum for other things? The SCRUM Fieldbook says yes, and cites examples of using Scrum in company mergers, car manufacturers and the army. However the cynic in me says that a book like this has to get to 250 pages somehow. I think that Scrum imparts the most value into the technology sector, but that in no way diminishes the value of individual parts of Scrum. After performing this deep-dive, I feel that many organisations can benefit from fast feedback loops, decentralised decision making and regular introspections and analysis on development or delivery processes. Good managers often make a difference becasue they embody these actions in their management philosophy, but good managers can also leave; implementing all or at least some of Scrum into your organisation's culture should last much longer.

