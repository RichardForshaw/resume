---
layout: post
title:  "AI: Fear, Facts and The Future"
description: "Media excitement about AI has been escalating in the last few months, especially as a threat to jobs. The basic facts being reported may true, but many important contexts and facts are missing, and often the angle is all wrong."
tags:
    - technology
    - AI
author: Richard Forshaw
---

The media has been latching on to AI and mostly ChatGPT for the last few months. Hype has been raised even further because of the recent announcements about ChatGPT-4. The obvious headline to run is that "AI will take our jobs", which has been a persistent theme for many years.

Wired magazine jumped on this bandwagon with a video analysing AI's ability to replace 20 selected jobs, and it raised my heckles with a mix of misdirection and poor argument framing. But my reaction wasn't all down to Wired - it was also interesting to see the opinions and attitudes of the people being asked to defend themselves against the new technology.

I think there are two questions that need asking - one is how realistic Wired's scenario is, and the second is whether the headline-driven fear of AI disenfranchising us is really valid.

![Robot ChatGPT Media Interview](images/ChatGPT_Interview.jpg)

## Jobs Under Fire

Let's look at a few examples of the Wired video (which you can find [here](https://www.youtube.com/watch?v=tTagNMmzgQo)). Wired took 20 occupations and put them in front of ChatGPT. The job's representative then asked ChatGPT to perform an aspect of their job and then evaluated the result. There were some odd choices of occupation (bartender, circus performer, comedian), but I think that did add some balance to the piece because news headlines generally do not specify exactly whose jobs are going to be 'taken'.

But here lies the first falsity: The article used ChatGPT as the "AI" in question. This is all fine but the article frames this entirely as "AI", whereas ChatGPT is only a specific type of AI: a Large Language Model trained with Terabytes of general information. I have used ChatGPT, as well as various AI image-generators, and the recurring theme I have found is that they provide answers which fit your general question very well, but not necessarily all the details. And many jobs come down to details.

Let's examine a few.

### Software Engineer

This one has probably been discussed the most, or at least I have seen the most discussion because of my profession. My experience is similar to the subject in the video, so I will respond from my perspective. I have used ChatGPT to write simple code for me and it has worked. I have been genuinely amazed by this and it has saved me a lot of time, mainly because I can spend more of my day thinking about the complex problems rather than the simple ones.

As a Software Engineer, a lot of code that I need is what I consider as one-shot 'rote' answers; this is code that is probably written hundreds of times a day around the world and while it takes up a significant portion of my time it only represents a very small percentage of the problem I am trying to solve. For this, ChatGPT is great, because it frees up my brain to keep the complicated context in my memory and not have to dump it out to solve the 'simple' stuff.

For this reason I embrace AI, but this is where I am also worried. It is obvious to me that millions of lines of code have been cut-and-pasted from StackOverflow (a popular coding question-and-answer site) with the side-effect that the developer in question may not really know how it works. I can easily see this happening with AI-assisted coding, where an engineer patches many 'simple' parts together and ends up with a complex mess that they don't fully understand.

### Doctor

The Doctor sat down and asked ChatGPT whether a set of symptoms he gave should be diagnosed as Monkeypox. His opinion that "AI cannot do my job" was influenced by the fact that the response, despite correctly answering the question, also gave the advice to go and see a healthcare professional. But here is where the AI vs ChatGPT misdirections comes into effect.

ChatGPT is not the be-all of AI, and ailments seen by GPs are not the only field that is being explored by AI. The medical imaging field is where many AI breakthroughs are being made, which use specifically-trained models, not general ones like ChatGPT. Trends from published research papers show that AI models sometimes slightly outperform trained humans and are usually just as good [1]. However there are still being gaps and challenges in the research [2]. Latest studies have also shown that combined human + AI analysis outperforms both [3], and that clearly seems like a good thing.

![Medical AI](images/medical_ai.jpg)

The other angle to look at is that [GPs often report being overworked](https://www.bma.org.uk/news-and-opinion/on-the-edge-gps-in-despair), and anyone having recently been to a public practice can attest to this by the amount of time allotted to your visit. If half of GPs' diagnoses are simple common ailments, then perhaps these can be handled by a suitably-trained AI whose accuracy is as good as a GP. Automating high-frequency, low-impact illnesses would surely free GPs up to spend more time on the non-trivial cases, and so ChatGPT's suggestion to go to a healthcare specialist for the video's example is in my opinion a preferred outcome.

### Lawyer

The Lawyer in the video requested to write a legal memorandum regarding the sale of health information. The response was given a pretty big thumbs-down by the lawyer mainly regarding the lack of information sourcing. I think this is a good reason to say that ChatGPT is not going to make a good lawyer, and it is known to make mistakes in what it produces (in researching the section on medical imaging AI, ChatGPT gave me URLs to reports which were incorrect). However once again the video is looking only at ChatGPT and not AI as a whole.

There are AI systems which are trained specifically for legal research and perform arduous legal tasks such as statute searches and legal document labelling very quickly. AI systems have been found to outperform trained humans in these areas (e.g. [4]). Context is important however, and these tasks are described as "a fixed length, low added value [and] monotonous". Which in my mind is exactly the type of work that humans typically want to avoid.

We also already know that the recent OpenAI paper on ChatGPT-4 claimed that it passed the US Bar Exam in the top 10th percentile. If this claim is independently verified, then even a Large Language Model outperforms 9 out of 10 law candidates. And, much like AI in medical imaging, lawyers who teamed up with specific legal-AI systems were found to perform better than either does alone. This reflects OpenAI's concept of an 'amplifying tool', allowing fewer humans to be more productive. So lawyers beware.

### Influencer

This example, though a less serious 'occupation' than the previous, reveals a character trait I think it prevalent at the moment, namely an attitude that AI will typically target a single person. The influencer asks ChatGPT to create an Instagram post for a particular photo and is quick to dismiss that the output is not written as she would specifically write it. I think this attitude is mistaken on many counts.

Firstly, the fact that ChatGPT recognises the subject matter of the photo and writes a post in the correct context is completely overlooked. To me this is amazing, that an AI can interpret an image and write about it was once the stuff of dreams. Secondly, any influencer should not be worried about if an AI can replace them specifically - the exercise is really to test if an AI can mimic being 'an influencer'. And I think it did this with flying colours. One only has to look at ['lilmiquela' on Instagram](https://www.instagram.com/lilmiquela/) with 2.8 million followers (and the fact that she valued her creator at [$125million 4 years ago](https://techcrunch.com/2019/01/14/more-investors-are-betting-on-virtual-influencers-like-lil-miquela/)) to see that human influencers have some real competition.

![Internet robot lilmiquela](images/lilmiquela.jpg)

Finally, while it is true that the output did not mimic her exact style, we know already that different AI models can mimic not only writing styles but also voices and other characteristics if fed with the correct data. in the case of voice cloning, currently takes only a few minutes of original samples, but in a recent paper Microsoft claims to be able to do this [with only 3 seconds of samples](https://www.youtube.com/watch?v=F6HSsVIkqIU)! Once again, the video incorrectly substitutes 'ChatGPT' for 'AI' and does not delver further into what is really possible.

### Fireman

This was perhaps the most interesting cameo of the video. The fireman simply refused to ask ChatGPT to do anything, stating categorically that an AI could not do his job. I was a little disappointed in this because, much like the bartender and personal trainer who appeared before him, he could have asked a question relating to his job such as 'design a leaflet to inform consumers about current fire-retardant products' or 'give me some information on smoke-alarm placement for this apartment layout'. Fire-fighters do not only reactively fight fires, they also proactively fight them.

I could see they were trying to make a point, but once again it suffered from the narrow-view of text-based LLMs. My thoughts immediately went to things like [Boston Dynamics' amazing Spot](https://www.bostondynamics.com/products/spot), which uses AI. First-responder services regularly talk about taking humans out of danger, and this is a space that AI and robotics are destined to fill. Who would argue with this? Although it would not be doing a fire-fighter's whole job, I'm sure there would be few arguments in using such a tool to do the riskiest or most challenging parts.

## AI: More than ChatGPT

AI is frequently being used in challenging environments. The problem is that these systems and applications are not sexy and don't get headlines. ChatGPT does get the headlines, but the reporting makes the audience think that this is representative of all AI. AI is much more than that, and I think Wired did a dis-service by mis-labelling the video.

It is also important to note that ChatGTP falls into the Large Language Model category of AI. Without getting too technical, at its core it predicts the statistical likelihood of one word following another in a given context. This is great at forming coherent sentences but you can question whether this is really 'intelligence' when compared to other forms of AI. This is why it makes mistakes in the details of its answers.

The only occupation of those I have listed above for which ChatGPT is a currently a good fit is developer, and with ChatGPT-4, this capability will only improve. (OpenAI claims that ChatGPT-4 will also respond significantly better for legal and medical questions, but in the context of Wired's video I'm just looking at ChatGPT-3.5.) Am I scared of this? A little - but mainly for selfish reasons. I still like programming and I find joy and satisfaction in it, much as a craftsman would in using their specific tools. But that is only part of what I do. I have not yet seen how AI can fulfil my entire role from customer to design & development to market and the feedback between them all. But if it helps me do that faster, why would I complain? I can still program if I want to.

Which brings me to whether jobs are really in jeopardy.

![humans and AI working together](images/human_robot_shaking.jpg)

## AI as Amplifying Tools

I am repeating this because I think it is good to focus on. Perhaps with the exception of artisans and craftsmen, the business world has always wanted to do things faster. Typically tools are invented to help us in performing our jobs. This is [precisely what technology is](https://en.wikipedia.org/wiki/Technology) - a way of advancing what we are capable of doing and creating. With the hindsight we now have, would we want the jobs back that robots and machines 'took' 30 years ago? From overworked GPs and lawyers, to risk-taking first responders, in 30 years will we be complaining if these jobs have been significantly improved?

AI is just more technology, but more powerful. I've worked at many companies and had many responsibilities. Some of those were of "low added value" and "monotonous", as described above. These words are a formal way of saying 'boring'. The output of the work may be valuable to someone, but the act of performing it is often un-inspiring and de-motivating. I would be happy to accept a tool which kept my boss happy by producing accurate output faster than me, and also made me happy by allowing me to work on more interesting things.

I think we are at a turning point of technology, creative potential and hopefully job satisfaction if we choose to adopt the right tools in the right way.  So let's not be scared with one-dimensional media arguments. Let's understand a bit better.

----

[1]: [Comparison of Chest Radiograph Interpretations by Artificial Intelligence Algorithm vs Radiology Residents](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7547369/)
[2]: [A review on deep learning in medical image analysis](https://link.springer.com/article/10.1007/s13735-021-00218-1)
[3]: [Doctors using AI catch breast cancer more often than either does alone](https://www.technologyreview.com/2022/07/11/1055677/ai-diagnose-breast-cancer-mammograms/)
[4]: [Evaluating Human versus Machine Learning Performance in a LegalTech Problem](https://www.mdpi.com/2076-3417/12/1/297)
