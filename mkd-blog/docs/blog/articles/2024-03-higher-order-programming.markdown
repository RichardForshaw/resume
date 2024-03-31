---
layout: post
title:  "Write Flexible Code with Higher-Order Thinking"
description: "Remember those high-level programming techniques that you thought you would never use? It turns out they can be useful after all, and can help you solve tricky problems."
tags:
    - Software Development
    - Programming Techniques
    - Python
author: Richard Forshaw
---

At university, I remember sitting in Advanced Programming lectures being taught about 'Currying'. I didn't really understand it then and I don't really understand it now. In fact I had to look it up in order to write this post: Currying is the process of taking a function that takes multiple arguments (the most basic example is probably is `add(x, y)`) and transforming it into a sequence of functions each taking one argument and returning another function (in our case something like `new_add(x)(y)`). In this way you can chain the functions.

Why would this be useful? I can probably see some applications for it, but as with many advanced techniques like this you probably need to spend three times longer explaining and understanding the problem that needs it, than explaining the actual solution. But sometimes these problems do come along, and if you haven't been taught to understand some core concepts of higher-level functional thinking then you won't be able to spot the opportunity to do something creative and flexible. Instead will find yourself throwing something brittle together while leaving yourself with the feeling of "isn't there a better way to do this?".

![Russian Dolls](./images/russian_dolls.jpg)

## The Problem

At Instatruck (as I'm sure with many other tech products) we run a few tasks both asynchronously and delayed, such as sending messages to customers. Recently a condition came a long where we needed to not only delay a task for processing, but executing it was also dependent on the state of the system. Specifically, if a customer's job was still not assigned to a driver after a period of time, we need to to send an external alert, but if it did get assigned then we didn't.

I think programmers tend to think in a procedural way, and so we tackled the problem like any other problem. Your first solution is always the worst and you tend to throw it away. I call it 'the pancake process', because when my wife makes pancakes she always throws the first one away because it's the worst. The 'pancake' in this case was just running a timer every minute to check the system status and make a decision. Like I say, terrible idea but to get better ideas you often have to start with a bad one.

## Bad Solutions

The second idea is what maybe many other people would try: queue the message, but whenever the system state changes, check if you need to cancel the message. This presents a few problems:

 1. you need to store the ID of the message to be able to cancel it from the queue. The original authors of our codebase took this approach with a similar behaviour and soon the code started holding more and more queued job references, making it very messy. How and where should the system store these IDs? What code entities are they associated with? How does this affect coupling and cohesion? (short answer: badly). To do this you really need a separate service to be able to manage the queue which we didn't really have time to write.
 2. scaling up with more messages means that you need to store more of these IDs. We already know this is not a good idea, but on top of that you are likely to need to keep creating new columns in your database. This is not very scalable, and in the case that you want to remove some of this behaviour, it means you need to clean your database up. One thing we should always try to consider as Software Engineers is the growing and shrinking of system behaviours.
 3. you need to handle all the logic for determining when to cancel a message from the queue, i.e. when system state changes. This logic can quickly become complex and also relies on the type of message being queued; if the behaviour in this example required 3 messages to be queued, then after some change of system state maybe only 1 or 2 need to be cancelled.

![Complex to simple](./images/complex_simple.jpg)

## A Simple Answer

As Albert Einstein said, "Everything should be made as simple as possible but no simpler". The solution that revealed itself to us was nice and simple in concept: just queue the message anyway and decide at the point of running it if it should still be executed. By doing this, you no longer need to:
 - store and manage any message IDs
 - create and maintain logic to handle the cases for cancelling queued messages (the message simply decides itself when it is popped from the queue if it should still execute).

This seems an elegant idea from a high-level, and solves all of the problems described above. But the implementation presents us with a new one; because different messages will require different conditions, how do you encode a condition with a message in a message queue? We are removing the need to manage messages in the queue, but we still need to know which conditions to check. We basically need to push 'code' into the queue. This is where the knowledge of higher-order functions comes in.

## Show me!

The solution is to define a function which accepts a condition on an entity as part of its parameters, and a function to call (with additional parameters) as the remaining parameters. In pseudo-code it would look something like this:

```
function conditional_dispatch_function(obj_id, condition_attribute, function_to_dispatch, args):
    # Load the object
    obj = load_object(id)

    # Test condition
    if obj.condition_attribute:
        function_to_dispatch(args)

```

If we were not using a queue, the we could just pass the object into the function rather than the ID. This type of function could probably be used to decouple a condition from an action in general, for example if you wanted to allow a user-configured list of actions and event. However in this specific case we cannot push the object onto a queue easily, and more importantly because of the delayed nature of the condition, we need to get the latest saved state of the object since this is why we have the problem in the first place.

Python provides some nice ways of doing this. The system under test is written using Django, so we can use that for our object retrieval. We can then use the `getattr` method to check our condition (assuming that there is a corresponding property on the object), and use the `__import__` builtin or the `importlib` library to locate our dispatch function and pass it the arguments.

```py
def conditional_dispatch_function(obj_id, condition_attribute, function_to_dispatch, args):
    # Load the object
    obj = model.objects.get(pk=obj_id)

    # Test the condition
    if getattr(obj, condition_attribute):
        # Access the function (simplified version)
        module = __import__(module_name)  # Dynamically import the module
        func = getattr(module, func_name)
        return func(args)

    return None
```

Now the `conditional_dispatch_function` can be queued in an asynchronous queue with its arguments, and the required condition can be executed when required. This is also easy to test because as long as the condition function and dispatch functions are tested, you know everything will work.

![Schwarzenegger](./images/arnold-double-biceps-banner.png)

## Collect Knowledge

I recently read the Arnold Schwarzenegger book "Be Useful: 7 Tools For Life". In Chapter 6 he advocates always absorbing knowledge. "Be Curious" and "Be A Sponge" are two of the sub-sections. You might think I'm writing this post as technical information, and there is that aspect to it. I think it's important to know about higher-level functional programming. But I also agree with Arnold: I think it's important simply _to know_... about many things. You never know when you might need something. In many of my Computer Science lectures, I had no immediate use for what I was learning (except for coursework and exams). But I also didn't know when I **would** need those things, and now I'm glad I learnt them. Even early in my career, I maintained an interest in things that I didn't need now, because I thought one day I would. And most time, I was right.


