---
layout: post
title:  "3 Kent Beck Insights That Are Still True"
description: "Kent Beck is a bit of a legend for programmers. His 2008 book 'Implementation Patterns', while focussed on Java and Object-Oriented programming, still has some important insights for all programmers to know."
tags:
    - Programming
    - Software Development
author: Richard Forshaw
---

I recently read Kent Beck's book ['Implementation Patterns'](../books/2023-02-implementation-patterns-kent-beck.markdown). While most of it is focussed on Java and OO-programming, there is still much that he talks about which is relevant to programing and software development as a whole.

Programming is hard, and developing large-scale long-lived software is harder still as it involves disciplines and behaviours that aren't taught in most programming courses, or at least they weren't when I was at University. Perhaps now there is more importance given to them, but in case there isn't here are three things from Kent's book which I think every developer needs to consider.

![Lightbulb Idea](./images/lightbulb-idea.jpeg)

## 1. Cost

When you step out of a programming course and into a software development team, you are entering a much different world than the one that you left. The one you left was concerned with how to tell a computer to solve a certain problem for you, whereas the new one adds time and cost constraints into the mix, together with the dreaded 'L'-word (Legacy), and nobody really prepares you for that.

Kent dedicates a whole chapter to software cost; a short chapter but a chapter non-the-less. As with any business department or function, cost will eventually become a driving force behind its operation. This is of course still true today but still not fully understood by many developers.

Costs come in many forms, and Kent cites [Yourdon and Constantine](https://archive.org/details/Structured_Design_Edward_Yourdon_Larry_Constantine/mode/2up), saying that the cost of maintaining a software system is usually greater than the cost of developing it (in this case the book defines maintenance as including bug-fixing and modification). This is most likely still true today even with modern engineering techniques.

As Kent says under his laws of programs: "There is no such thing as 'done'". These days we tend to be aware of this fact, but he breaks this maintenance cost down even further, saying that it it is made up of:

 - Cost of understanding
 - Cost of changing
 - Cost of testing
 - Cost of deploying

On the first of these, Kent says "Learning what the current code does is the expensive part". This is certainly true today, because software engineering is still knowledge-work, and knowledge-work requires a depth of understanding prior to execution. Sadly much of this understanding is still lost when transferring a system, module or even function between developers and my career has seen many and continued attempts to fix this.

It is worth understanding the impact of these costs but you should also recognise that the costs are just a symptom - an indicator (albeit a critical one) that allows us to see where there may be another problem lurking.

Two approaches to lower these costs that may be elicited from Kent's book are:

 - fix the cost of understanding by improving communication; and
 - consider that costs can be reduced if there were less things to change or overhead to change them

We will look at these both below.

## 2. Communication and Naming

Communication is one of the most underrated properties of software programs, but one of the most dualistic. I wager there is not a developer reading this who has been frustrated not being able to understand another developer's code as quickly as they wanted. But by inference, it means that the code they have written has caused the same frustration. As demonstration, I willingly put my hand up and admit that I have re-visited code I have written within 12 months and been initially confused as to what it is doing.

![Two networked developers](./images/two-facing-developers.png)

One of my favourite quotes from Donald Knuth is this:

> "The best programs are written so that computing machines can perform them quickly and so that human beings can understand them clearly."

And personally, I would not lose too much sleep if the "computing machines" do not perform them quickly, since not all programs need to run fast but _they all need to be read by other programmers_.

The biggest influence we have over a computer program, aside from how it is designed, is the words that we choose when writing it. Kent and I share the values that communication, and by extension, naming variables, functions and classes are among the most important considerations and deserve thought.

> "Finding just the right name is one of the most satisfying moments in programming"

It is good that your algorithm keeps thousands of messages running through your system, but if the next developer to maintain your code doesn't realise its function easily then it is likely to spell trouble.

Kent's advice is:

> "Convey purpose, type and lifetime of the variable to readers"

I admit that even I learnt something when reading this as I would rarely consider considering the lifetime in this equation, but it is important and often indicates the relevance and importance of a variable within the code.

A worthy example of appropriate naming is in Kent's description of an "Explaining Message". This is defined as a message (i.e. a method on an object) which distinguishes between its intention and its implementation. Specifically, Kent recalls when he saw a method defined like this:

```
highlight(Rectangle area) {
    reverse(area);
}
```

"Why is this useful?" he asked himself... why not just expose `reverse()` on the object. But this displays exactly what is meant between _intention_ and _implementation_. The intent (i.e. you could say the API action that is useful to the user) is to _highlight_. Internally however, it is implemented as reversing the area of the given shape. Subtle but very useful.

## 3. Change and Trade-offs

The other way of looking at reducing the cost of maintenance is to reduce the likelihood of change that will be required. If you incur a cost per change then you can either reduce the cost (as above) or reduce the number of changes. This however is a slippery slope.

In saying this, we are advocating for introducing _flexibility_ into the system, but we must recognise there are two types of flexibility:

 - one driven by the actual requirements
 - one driven by second-guessing future requirements

Kent points out that flexibility comes with a cost, and usually introduces complexity which may be unnecessary:

> "Programs should be flexible but only in ways they change. If [something] never changes, all that complexity is cost without benefit."

This shares much with another of Donald Knuth's famous quotes:

> "Premature optimization is the root of all evil."

![Complex and Simple](./images/ComplexSimplex.png)

Kent uses a feature of OO to demonstrate this in the section about behavioural messages. One beautiful thing about OO programming is polymorphism, a feature allowing conditional decisions to be made at run-time in an elegant way instead of what he calls 'explicit conditionals' (i.e the control-flow statements built-in to the language). Explicit conditionals are easy to read but provide little flexibility when it comes to extending behaviour. Polymorphism provides a method to control the execution flow in a more flexible way which does not require existing code to be changed (basically the [Open-Closed Principle](https://www.oodesign.com/open-close-principle)).

Kent however recognises that while this makes code more flexible, it requires more skill to read, understand and write, and introduces problems in communicating to other programmers. Thus it is a trade-off in the change domain.

The association of flexibility with complexity is one of programming's many great trade-offs, and because of this flexibility should be introduced judiciously. One approach to this is by doing agile development (and doing it correctly). Because agile (e.g. Scrum) involves releasing working software often, you must make the flexibility vs simplicity decision early and within your delivery cadence constraints. I suspect that this will typically come down on the 'simplicity' side, and thus validate Kent's statement that:

> "The time to introduce flexibility is when it is definitely needed"

Instead of over-complicating with too much flexibility, Kent advocates for choosing simplicity and effective testing. I am a big proponent of TDD and automated testing and there have been many occasions where an effective suite of tests have given me confidence in being able to change code implementation safely and quickly. But only when it is needed.




