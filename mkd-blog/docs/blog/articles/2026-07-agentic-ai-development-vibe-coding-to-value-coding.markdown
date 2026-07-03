---
layout: post
title:  "Vanilla AI agents aren't good. You need to invest in toppings."
description: "If you are getting started with agentic development or AI integration, don't just dive in with plain old agents. LLMs need your valuable context! Here are some tips."
tags:
    - engineering leadership
    - CTO
    - agentic development
    - spec-driven-development
    - ai
author: Richard Forshaw
---

Gone are the days of typing simple questions into an LLM prompt, asking it to write you a poem, or make you a travel itinerary. Plenty of people still do this, but now that LLMs have proven their chops in writing code, we are now firmly in the agentic age of using LLMs to automate our processes.

But as with the integration of any new technology into existing environments, things are not going smoothly. Whether that be through misunderstandings or misalignments, there is evidence of adoption gone wrong, resulting in claims of 'AI is not ready yet'. But what I think is really happening is that organisations are not yet ready.

I am mostly interested in the harnessing of new technology with engineering rigour in order to provide real long-lasting value, and it seems like many companies are passing through these crossroads at the moment.

![Image of disorganised light entering a prism and becoming organised](./images/enhancing%20prism.jpg)

### The TL;DR

Using off-the-shelf vanilla agents are a cause of failure for organisational AI integration because they are lacking your specific context. To succeed:

 - effort must be invested in codifying your business environment (domain language, tech stack, processes) to help the agents shift from 'Vibe Coding' to 'Value Coding'
 - maintain your good engineering principles, like iterating and pausing to review specs; don't throw everything over to the agents
 - use the 3 "C"s: to *critique*, *collaborate* or *create* to identify how much AI to mix in to your teams


## The Recent History: Why are AI Agents Failing?

To get to the vast plains of wide adoption, we had to pass through the valley of Vibe Coding. I attended a start-up presentation last year promising to show me how to use AI to launch my startup in hours, not months.

At the start of the presentation, we were all put on tenterhooks by the engineer typing a simple (maybe 100 word) prompt into an LLM (I can't remember which one), asking it to make a web-app (I can't remember the specifics), but also asking it to make it 'modern', 'flashy' and 'responsive'.

The results were indeed impressive... until the user tried to do anything beyond the first page, upon which a cascade of errors ran through the terminal as the engineer tried to quickly address the issue. The entrepreneurs and product managers in the room went from delight to disappointment, and as my inner-engineer kicked in, I saw the familiar `CORS Error` message in the terminal, and I thought: How can these advanced agents not handle fixing an error that every new web developer faces?

Vibe coding still has its place, but after a year of seeing LLMs produce games and websites out of thin air, there soon followed a swathe of requests asking "why doesn't this work in production". One colleague of mine reported their consultancy being approached by a client asking "how do I make my app work... out there?" (by which they meant deploying it to an app store). After a few questions, it was clear that it wasn't anywhere near ready for that yet.

This is why we need to move from "Vibe to Value". In my opinion, this is a mixture of a few things, including prompt maturity and true collaboration through shared understandings. And a lot of this boils down to context.

So what do we do about it?

## Why Context is King for Productive Agents

LLMs and agents (which run LLMs underneath) are pretty useless really.

Wait... what do I mean? Oh... I know what is missing. My context!

LLMs and agents (which run LLMs underneath) are pretty useless when they are asked to do things without any context of the environment they are being applied to. The reason why is quite simple. Because they are essentially statistical prediction machines, and they are trained on all the knowledge of the internet, then they will follow the statistics of the internet.

There, that's better now that you have more context. Don't you think?

![An ice-cream themed depiction of average statistical knowledge of AI LLMs](./images/Ice%20Cream%20Bell%20Curve.jpg)

Without your specific context, LLMs will happily trawl through the average content from the internet, which is great for general advice but not great when you want to collaborate with it on your specific toolkit and deployment pipeline.

What does this look like? Hallucinations, wasted time and rework. Just like if your team members don't understand the brief. The interesting thing is that these are not necessarily 'hallucinations', it is the LLM reverting to the mean. It's the fact that you're starting with a vanilla ice-cream

However, once the agent is topped with the sprinkes and sauce of your specific context, things become much better.

## Induct your Agents

This is why I think agents need to be 'inducted', just like real employees. They need to know about your specific environment; your toolkit, your platforms, your processes, your quality gates, your output expectations. If you were to on-board a new employee, they would learn most of these on-the-job, or maybe you would have hired them because they already have some of those skills through their recent experience. They generally acquire context and retain it.

That we mistakenly assume this is also true of Agents is down to two things.

One is a symptom of the [Illusion of Transparency](./2026-06-behaviours-for-ai-driven-development.markdown#the-illusion-of-transparency) which I mentioned in a previous post. We often oversell ourselves on how much information we have conveyed to someone else. The other related thing is that the LLM marketing hype has oversold us on what LLMs can do; most of the videos show a short and simple prompt being typed into a magic box, and then something amazing being created.

This is not how it works. Like most technology, it won't work well out of the box. You need to provide the context.

## Personas, Skills and Context Files

You might have seen people talk about personas, skills or 'Gems'. These are often LLM-specific, but a 'persona' is quite common. This is simply a prompt that tells an LLM how to behave. You can put many things in this prompt. For example:

 - I have a job-matching agent which I instruct to act like a hiring manager, inform me of the matches and gaps between the job description and my resume, tell me what they would expect to find in my cover letter and what questions they are likely to ask.
 - I had a French Tutor agent, which I instructed with what level I wanted to converse at, what topics I wanted to talk about and how terse or verbose their responses should be.
 - I have an SQL assistant which knows the basic schema of the database, the database and version we are using, the major business-language entities and the ORM we are using.

All these add context to the queries that you then ask it. The SQL assistant has barely ever been wrong.

Beyond this, when I started using Spec-Driven-Development with SpecKit, I noticed how it maintained a master 'Constitution' which it applied to the overall development. As I delved deeper and deeper into SDD, I saw extra value in maintaining more and more context for the agents to refer to.

Some examples of context files that I have created are:

 - The Domain Language of your business: Who are the actors, what are the major system entities, what are the main events?
 - The Development Environment: How do you develop? Is it local or in containers? What language and frameworks do you use? Do you have something niche or bespoke that you use? What key environment quirks do you have?
 - Your Process: What process do you enforce? Do you use TDD? In which case do you want to enforce Red-Green-Refactor loops? Do you use Gherkin scenarios? In which case do you need to stop and review them with the team before proceeding to implementation?

This is all important context which have been proven in your development environment so far, so how should an autonomous LLM be expected to integrate with your team if it doesn't know about it?

![workers on scaffolding](./images/climbing-scaffolding.jpg)

## Good Engineering Behaviour

The other thing that has helped to improve my own results is simply sticking to good engineering behaviour. There are skills we have as engineers which may be so ingrained in our daily practices that we don't realise it any more. Here are some examples:

### Seeking to Understand

The best leaders seek to be understood and the best engineers seek to understand. However a vanilla AI agent doesn't do this; it seeks to deliver on your goal and make you happy as fast as possible. I have found that most downstream issues I have had with using agents simply comes from a lack of understanding.

This is why I love the "Grill Me" skill by [Matt Pocock](https://www.youtube.com/watch?v=v4F1gFy-hqg). I use this often, right at the start of my interactions. The point is to *have an intense discussion* with the agent and force it to ask questions. Once the discussion session is complete, it is trivial for an LLM to then convert this into a set of bullet points for other agents to use. I think it has saved me many hours of back-tracking.

This is also why I still use BDD with agents; working on behaviours is still a sound way to iterate on a product, but the use of Gherkin scenarios is an excellent interface opportunity between a specification that is both human- and AI-readable.

### Iterate

Another mistake I made was to assign a huge development task to agents. Even though I was using SpecKit and the process seemed to be on track, I found the agents to be deviating from my expectations. This is partly because of the lack of understanding, but also because the goal was too big. [Iterating is still valuable](./2025-10-why-we-iterate.markdown), and building what you want incrementally with the biggest value first is still important.

Iterating also allows you to insert human checkpoints into the process, allowing you to review, respond and redirect if necessary. Again, this has been proven to work in real life, and you wouldn't assign a mammoth task to a new junior hire, so why do it with an agent?

### Define your mix

I use AI for a number of things, and in an number of roles. You don't have to bring AI on board and run the whole show. There are always pockets of value to be had at the start and a pathway to expansion. This is essentially iterating on your adoption.

For example, I didn't start by letting AI agents loose on a project from the get-go. I looked for value in the following places:

 - Writing test scenarios based on new behaviour, so developers didn't have to
 - Assisting with code-review, and then fine-tuning and up-skilling this behaviour
 - Writing code for single PRs

These are also examples of using AI for the 3 "C"s: to *critique*, *collaborate* or *create*. I started in this order... first of all critiquing (e.g. code reviews). Then collaboration (assisting with writing test scenarios) and finally creation (write all of this code for me).

I spoke to someone yesterday who has just started orchestrating a team of agents to go from new feature requirement to deployable code, but that wasn't his entry point. He has been using and learning the skills needed to be able to do this, and is now comfortable to let his agents loose. But he didn't jump straight on to a MotoGP bike; he had to learn to cycle first.


## Conclusion

The short advice is: don't just throw off-the-shelf AI agents into your environment. You need to induct them; identify the context that your teams are already working in and make sure that the agents are using the same. (You will often find that codifying this context is beneficial to your team as well.)

Also don't forget that good engineering practices still apply; understanding and iterating on a problem has brought value for decades, and these techniques should not be thrown away.

Finally, remember that you are in control of how you mix your organisation and your agents. Move through the 3 "C"s (critique, collaborate and create) in order to gain confidence and get buy-in.

This way, you will take your bland-tasting vanilla agents and slowly and deliberately adorn them with all the right toppings to get the mix that is right for you.
