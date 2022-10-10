---
layout: post
title:  "I Love Pipelines"
description: "I love queues, and I think I love pipelines more. Software pipelines that is. What's so great about them? In here I try to present the benefits to using pipelines in your code."
revision_date: "2022-07-21"
tags:
    - Programming Techniques
    - Data Structures
author: Richard Forshaw
---

Perhaps its because I'm half English, but I love queues. But because I'm a software engineer, what I really mean is **software** queues.

Queues are one of those software constructs that are very easy to explain because they come with a direct mapping to an everyday concept. Sometimes it is difficult to explain a heap, or a map, or a class. But a queue - people just know what it is.

## From Queue to Pipeline

![pipeline](images/pipeline.jpg "Pipelines")

Perhaps it's because I spent a lot of time around mining industry people that I also love pipelines. Pipelines are a little more difficult to explain but people generally get the concept. Pipelines and queues also fit together nicely.

If you don't know what a pipeline is in software, it is conceptually the same as a real-life pipeline in that it is a structure that has an 'in' and an 'out' and a direction of flow. Very much like a queue in fact. The difference is that a software pipeline is also made up of multiple sections, and more specifically to programming, each section has a function to transform the data that flows through it. Thus the data that comes out of the pipeline is a large transformation of the data that went in.

What's so great about that I hear you ask? How is that better than just writing one big function to manipulate my data? Well, breaking the transformation into steps allows you to focus on each step and what it does, and make sure that the output from one section is then able to be input into the next section. When you put all the sections together you have a pipeline which performs something complex, built up from simpler parts and chained together. And that is very powerful.

'So like a production line' you say. Yes, perhaps it could be called a production line, but I think pipeline is better because you can put pipelines together to make even bigger pipelines, whereas what comes off a production line tends to be the final thing which is not modified any more.

## Pipeline Power

So what makes this so powerful in programming? The great thing about this concept is that each part of a pipeline is a small function which maps very easily to the concept of a software 'unit'. This means that not only does this allow you to write unit tests at a much more granular level, it also makes finding errors in your transformation function easier.

Imagine you have a 3-stage pipeline - for simplicity's sake it calculates the formula `(x + 5)^2 / 4`. Your pipeline stages are therefore:

 * A function to add 5
 * A function to square a number
 * A function to divide by 4

Now bear with me - I know this example is very simple and you could write it as one function but the simplicity is just to demonstrate the sequential function execution. Writing this as a 3-step pipeline allows you to unit test each function to make sure it is working as a 'unit'. This has numerous benefits, for example:

 1.  As already briefly mentioned, it **maps beautifully to the concept of unit testing**. There is really not much more to be said about this; it is simply good practice to write your code as testable units and then test it at the same level.
 2. There are many inflection points and points of testing interest, and **using a pipeline can separate them**. If this were a single function then if you wished to test each one you would need to replay any previous calculation. Testing the `(x+5)` step for positive, negative and zero numbers is straightforward, but testing the squaring step with a zero input will specifically require you to write a test with the input of `-5`, which may be confusing and difficult to explain clearly to readers of your tests. And then what happens if the first calculation is changed to `(x+3)`? In order to perform the same functional test on the squaring step, you now need to modify your test which ensured that squaring of `0` was tested.
 3.  Testing of subsequent steps **relies on the previous steps functioning correctly**. If you wish to test that the final step returns `0` when provided with a `0` (i.e. `0/4`), you need to have confidence that the previous steps are functioning correctly. Using a pipeline, you can test each step separately.
 4. Testing of subsequent steps also **relies on previous steps being present**. Imagine inputting `-4` into the test. The expected outcome is `0.25`, right? But you will also get this answer if the squaring function has not been implemented yet. So how do you know if it is working? I've seen many bugs where part of an algorithm is not functioning or has not been implemented but overall it looks like it is working.
 5. **Adding an additional step** somewhere in the sequence is difficult, especially if the overall function is large. It is likely that all your existing tests will need to be re-written to accommodate the modified formula, and your overall confidence level is likely to go down. Using a pipeline makes this easier.

So writing this as a pipeline and testing the steps separately solve these and other problems. Of course for this particular problem it is probably overkill but hopefully it demonstrates my points.

## Examples

![Examples](images/pipeline_parts_thin.jpg "Some examples")

Here are a couple of demonstrations for using pipelines.

#### Javascript

For this I am using the very handy [pipeline-js](https://github.com/kamranahmedse/pipeline-js) package, which is internally very simple (using a sequence of promises), however creating a pipeline framework is not in the scope of this article; I will focus on usage instead

```
// For this example use the very handy pipeline-js
var Pipeline = require('pipeline-js');

// Our functions
function add5(x)   { return x + 5; }
function square(x) { return x * x; }
function div4(x)   { return x/4; }

console.log("Make pipeline...")
var pipeline = new Pipeline([add5, square, div4]);

console.log("Push 5 through pipeline: " + pipeline.process(5));
```

Ad you can see, for very little extra code, we can add our functions (using the previous example) to the pipeline and run it. The pipeline will execute each function in sequence, and pass the output of one stage to the input of the next.

#### Python

For the python example we will use the very useful [reduce](https://docs.python.org/3/library/functools.html#functools.reduce) function. I recommend everyone learn how to use `reduce`. This use case is a bit special because we want to execute a different function at each stage, so we achieve that by writing a `lambda`; because functions are first-class citizens, we can pass our pipeline functions around so they get executed.

```
from functools import reduce

# Pipeline functions
def add5(x):
    return x+5

def square(x):
    return x*x

def div4(x):
    return x//4

# Use the cool built-in 'reduce' function
output = reduce(lambda input, func: func(input), (add5, square, div4), 5)
print("Push 5 through pipeline: " + str(output))
```

This may be a little hard for new 'reduce' users to get their head around, but it very useful to know. In essence:

 * we provide `reduce` with a list of our functions (`add5, square, div4`) and a starting value ('5')
 * we then ask it to call each function and pass the output of one into the input of the next.

 Sexy stuff. This is a very simple example, and in the past I have adorned this to be similar to the javascript pipeline package where the pipeline is a class which encapsulates the 'how' of the pipeline, but the above still works.

## In Real Life

I have used pipelines successfully for the following problems:

 * **CSV input parser:** If importing data from a CSV file, it is likely that the data will need to be located, transformed, validated and enriched or decorated before it can be used in your system. A pipeline is excellent for performing these as a series of complex but testable steps
 * **Pricing calculator:** A system I managed has a complex series of steps for calculating prices, including steps based on tier/category, day of week and floor/ceiling prices as well as adding tax and service charge. Things became even more complicated when a 2nd product type was added, and the time was ripe to re-implement it as a pipeline per product which re-used certain components
 * **Data transformation pipeline:** When working on an optimisation problem, the inputs first needed to be validated, then undergo normalisation, simplification and finally have the solution engine applied. This was again a perfect opportunity to use a pipeline to chain together the individual stages, so each could be tested in isolation, especially since the whole pipeline was too complex to test as a whole.

In each case, when I have needed to hand over to another developer for them to enhance something, they have been able to quickly understand what is happening and have found it much easier to focus simply on the stage they need to modify rather than having to understand the whole pipeline.

## Advanced Pipelining

![Advanced pipelines](images/pipeline_complex.jpg "Advanced pipelines")

'But' I hear you ask again, 'why is this any different to writing a wrapper function which does the same thing? Well yes you could define all your function 'steps' and then just call them in sequence in a wrapper function, but doing that requires a bit more overhead and provides a bit more flexibility. Here are some advanced things that you can make your pipeline do:

 1. **Separate your pipeline specification from your code**: You can simply stuff your pipeline functions into an array (or tuple) and pass that to your pipeline builder. Your pipeline functionality can be nicely encapsulated and tailored to your application requirements.
 1. **Programmatically alter your pipeline**: Having done the above, you can modify your sequence based on some parameters of your current context. Do you need to have multiple pipelines depending on your context (e.g. the pricing calculator above)? Or do you need to add an extra stage depending on context (e.g. for different file formats)? You can dynamically modify your pipeline according to the contextual requirements
 1. **Turning parts of the pipeline on and off**: Does the customer need control over how their data is processed, or have they opted in to certain platform features and not others? You can read their configuration to turn stages on and off, or perhaps even alter their behaviour.
 1. **Re-using functions**: Using pipeline stages provides a great opportunity to re-use functions. In the case of the pricing pipeline, application of tax was done for each product and so was easily re-used. Beyond this, the re-used functions can be slightly modified depending on configuration using partial-functions (another programming feature worth learning) to avoid further re-writing.
 1. **Configuration to do all the above**: similar to customer configuration to enable or disable pipeline stages, any type of configuration can be used to modify the pipeline's stages, order or behaviour using simple constructs (maps, partials, array splicing...)

So there you have it. Go forth and unleash the power of the pipeline!


