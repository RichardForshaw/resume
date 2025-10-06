---
layout: post
title:  "AI Psychosis: Who is really the delusional one?"
description: "The term 'AI psychosis' is gaining traction in the media. It's true that some people are susceptible to this, but who is really suffering from the delusions?"
tags:
    - AI
    - Non-technical
author: Richard Forshaw
---

AI chatbots are confidence tricksters.

They aren't on the lookout for a payday (or some might argue that their creators are), but they behave in the same way. That's just how they are trained; to be sycophantic best-buddies, which often involves re-enforcing your belief in what you already want to be true. This has recently had some disasterous consequences for people who are more easly open to suggestion and persuasion. The sort of people who might be targetted by confidence tricksters.

The obvious question you are probably asking yourself is... why should anyone believe all the things that a chatbot is saying? After all, you don't, right?

![Robot in therapy](./images/robot-in-therapy.png)

## AI Psychosis

I listened to a [podcast about "AI Psychosis"](https://www.theguardian.com/science/audio/2025/aug/28/ai-psychosis-could-chatbots-fuel-delusional-thinking-podcast) (note: a media term not a medical term), which discussed the rise of chat users suffering from delusions induced by their chat interactions.This ranged from believing that the chatbot revealed a deep truth about reality (e.g.that we are living in a simulation), to forming a deep personal connection with the chatbot to the point that they thought it was looking out for their best interests, even if it involved harming themselves.

It was at that point I realised that the chat user is not the only one who is delusional... it's likely that we all are.

Is this an intentional inflamatory opinion? I don't think so. Most of us have been suffering from this delusion for many many years, and effects us every day. It's just that the impacts are usually pretty small. That delusion is bias - the "consensus bias", thinking that others act and behave the same as us.

## The Industry Delusion

Why is this important? It's been happening for a long time and the effects are becoming more and more serious.

We are all guilty of making assumptions about others. I do it all the time, especially as a parent. I think that my children already know how to tidy their room, or put things away after using them, simply because I already know these things. It takes mental effort to remind myself that this is not always true (sometimes, they are just being lazy).

Say you are a UX designer. You may have designed something that seems obvious to you, given your knowledge of user interfaces, but then you discover users complaining about your design being hard to use. How on earth can this be true?

This bias has already surfaced in data science and AI. One aspect has been documented in the book ["Invisible Women" by Caroline Criado-Perez](https://www.penguin.com.au/books/invisible-women-9781784706289), which talks about data not only being interpreted but also collected from a predominantly male perspective, mainly because the majority working in the field are male. There has also been several cases where AI training data was [shown to be been skewed](https://www.crescendo.ai/blog/ai-bias-examples-mitigation-guide) in a manner which perhaps reflected the make-up of the engineers working on that system. With the rapid uptake of AI to perform 'mundane' tasks, what other biases are present in our daily lives?

To me, the issues being raised in this podcast and other articles are indicative of two types of delusion. Firstly there is the unfortunate delusions that are being discussed: those suffered by the chat users, ranging from simply thinking that the AI is sentient (which has also been recorded by a senior Google engineer) to more serious examples. But secondly, I think the major AI companies are also under a delusion, being that the audience using their product is just like them; smart, well-educated and healthily sceptic about the information that comes out of a chatbot.

![mandelbrot set clip](./images/mandelbrot-set-10-satellite-valley-wide.jpg)

## The Limited Model

This healthy scepticism comes from having a knowledge of their internal workings. At its core, an AI chatbot is a probability machine which operates on the largest data set in human history. It has access to an unfathomable amount of information with which to execute its models, but it is also lacking a certain amount of context and congnitive ability.

For example, they cannot detect sarcasm nearly as well as humans can. This is not only in the context of the interaction with a user, but also in the information it is ingesting into its training data. Consider the following:

 * A message in a forum saying "Of course, if you believe hard enough when you jump off your roof, you will be able to fly!"
 * A user question: If I believe hard enough, will I be able to fly?
 
When you and I read the forum message, we will very likely have our sarcasm-detectors ringing very large bells, and if our friend were to ask us that question, we would tell them that they are asking a silly question - the answer is obvious. But an LLM is a pattern-matching probability machine. Combined with its bias to make the user happy, it is likely to answer that of course this is true.

One thing that fascinates me as a software professional is how these probability machines dip their toes into the ocean of Chaos Theory. Consider a (simplistic) example with the starting phrase:

"Of course, it is..."

When the LLM runs its statistical models and finds that the word 'possible' occurs next 34% of the time and the word 'not' occurs 39% of the time. However, given the context (I invite you to add your own), these two branches would then unfold into vastly different outcomes. In some examples, one of the branches may just be plain wrong.

## Our Internal Battle

You might think that humans are smarter than I'm giving us credit for, that we should know that we are interacting with a piece of software, just like the dozens of apps and web services that we use every day. The problem here is two-fold.

FIrstly, humans love to anthropomorphize things. We can't help it. We love to compare things to ourselves and talk about certain phenomena in terms of 'knowing' and 'thinking'. My favourite example is how many people talk about how smart spiders are when they see a web full of insects that is next to an outdoor light. "What a clever spider... it built its web there becasue it knows that insects are attracted to the light!". In reality, this is just luck. If you look closer there are other webs further away, but they have probably been abandoned. When we see this we don't talk about how stupid those spiders were!

Secondly, in order to be an effective productivity and collaboration tool, of course the best interface will be a discussion-based interface. After all, the next evolutionary phase will be for us to just talk to a chat interface and tell it what we want, and then receive the information in the most natural format: speech. So it is in the AI companies' interest to make their models communicate like humans; the more convincing the better.

This causes a battle within us, between the rational part which knows that this is essentially a programmed machine, and the emotional part which responds to the anthropomorphic nature of the interface. Don't tell me that you have never, even briefly, thought "wow, this thing is pretty smart if it knows that!".

![Diversity and AI](./images/diversity_and_ai.png)

## Our Future Relationships

The truth is that these products are being used by hundreds of millions of people, and we can't possibly start to believe that we know how all of them are likely to behave when interacting with a chatbot that is designed this way.

What is the current solution to this problem? Most chatbots have a tiny and succinct disclaimer under their prompts which inform us that chatbots can make mistakes and shouldn't be relied on. But this is shifting the responsibility to the user and is like a putting up a tiny 'please don't fight' sign in front of the giant battle between our rational and emotional selves.

What should we do about it? I'm certainly no expert and I only have opinions. As users, we certainly need to be aware that we are talking to software, but as discussed above this can be difficult. One potential trick is to limit the amount of time we spend talking to a single chat instance. 'Context Rot' is a known phenomenon that can begin to degrade the quality of the interaction the longer it goes on for. But the flip-side of engaging in a chat for a long time is that the personal connection is likely to become more pronounced simply because of the information already in the current chat context. These two properties are likely to increase but also become harder to detect. By regularly starting a new chat, this appearance of personal connection can be re-set and may provide us enough of a jolt to realise that we aren't talking to a sentient being.

On the other side, the opportunity rests with the AI companies to do better in removing "consensus bias" from their organisations, perhaps partly through training and partly through diversity of hiring. I don't claim to know the cultural make-up of these companies, but it seems to me that embracing diversity and inclusion both in the organisation and its data policies (including involving trained psychologists) will have a positive impact in eroding any biases encountered in engineering and deploying its products, and keeping us all safer.
