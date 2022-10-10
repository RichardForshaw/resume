---
layout: post
title:  "Getting To Know Modern Javascript (and You Should Too)"
description: "Last year I undertook a large project in Javascript, and I was able to dig a bit deeper into the language, instead of just using it to manipulate web pages. I noticed the same thing happening, and I have been since reminded about how many cool things you can do in JavaScript these days to write clean, compact and concise code."
date: "2022-10-06"
revision_date: "2022-10-06"
tags:
    - Programming Techniques
    - Javascript
author: Richard Forshaw
---

My origins were in C and C++, a highly imperative step-by-step language, and my brain usually still operates in that way. I have since been widely exposed to Python, and I now enjoy much of Python's built-in concise functional-style syntax, but I am aware that some of the features require a little extra understanding. Ultimately, I think my code is better for it, and probably faster too, taking advantage of the language's built-in features.

Last year I undertook a large project in Javascript, and I was able to dig a bit deeper into the language, instead of just using it to manipulate web pages. I noticed the same thing happening, and I have been since reminded about how many cool things you can do in JavaScript these days to write clean, compact and concise code.

Before these concepts were available in Javascript, I used to use them in coffeescript, but underneath they were translated into vanilla Javascript. Now they are supported directly by the language. Below are some of the things that I noted down as I was being exposed to more language features. I encourage you to give some of them a go, especially if you are also used to working in an imperative or 'old-javascript' style.

![Think about javascript](images/think_javascript.jpg)

## Simple stuff

### Creating Arrays

So you want to create an array? Not just reserve some space but populated with some data? I remember the days where this would involve one or more for-loops while you added data in a very imperative way. Python allows you to create arrays with simple data inside (often from another array-type data source) very simply with list comprehension, but I hadn't come across anything similar in JavaScript. Until I discovered some very useful `Array` methods.

Remember when you populated an array like this?

```
// Create [1, 2, 3, 4, 5, 6, 7, 8, 9]
var myList = [];
for (var i=1; i<10; i++) {
    myList.push(i)
}
```

Oh my, those were the days. C programmers rejoiced (yes I used to be one). Perhaps you installed [lodash](https://lodash.com/) (which was indeed very useful) to make it more concise:

```
// Create [1, 2, 3, 4, 5, 6, 7, 8, 9]
var myList = _.range(1, 10)  # Woo-hoo, 1 line!
```

But then your dependencies got bigger, and you only used 2% of lodash (or equivalent library). And for anything more complex than a simple progression of values, the contents of the `for` loop got bigger and bigger.

Then I discovered [`Array.from`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/from). This allows you to create arrays just like lodash, but is so much more powerful. Sure you can do the same as the example above:

```
// Create [1, 2, 3, 4, 5, 6, 7, 8, 9]
var myList = Array.from({length: 9}, (x, i) => i + 1)
```

But, as you can see `Array.from` takes parameters and a function, which means you can be more creative in constructing arrays:

```
// An array of squares:
var squares = Array.from({length: 5}, (x, i) => i * i)

// An array of negatives
var negatives = Array.from({length: 10}, (x, i) => -1-i)

// An array of test objects
var testObjs = Array.from({length: 5}, (x, i) => {
    return {id: i+1, testField: 'Test1', testString: String.fromCharCode(97+i).repeat(i+1)}
    })
```

Do exercise caution though - obviously it is easy to get carried away with the function definition and your code may quickly become much less readable. In this case I suggest breaking out into a function and creating your arrays like this, which also means code can be reused:

```
// With a buildTestObj function defined somewhere
var testObjs = Array.from({length: 5}, buildTestObj)
```

Just to round it off, the [Mozilla documentation](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/from#sequence_generator_range) also shows you how you can write your own lodash `range` function in one line using this function. Neat.

But that's not all - `Array.from` accepts an iterable in order to build an array, so you can generate arrays based on other arrays for example:

```
// otherdata = [{id: 102, name: 'a thing', price: 89}, {id: 36, name: 'another thing', price: 24}, {id: 98, name: 'thing3', price: 77}]
var ids = Array.from(otherData, x => x.id)
var prices = Array.from(otherData, x => x.price)
```

Note that it accepts an _iterable_ such as a string or a Set, not necessarily just another array. Creating an array from an iterable allows you perform array-type operations on that thing.

### Basic Object Creation

Just like creating custom arrays, how did you used to create objects? Probably something like this:

```
// Create a custom object
var myObj = {
    anInt: 1,
    aString: 'a string',
    anArray: [1,2,3,4]
    # ...
}
```

What about if you are copying an object, or populating from a map? Probably iterating over the items?

```
// Create from another object
var myObj = {}
for (item of myMap) {
    myObj[item[0]] = item[1]
}
```

How laborious.

With a little investigation, you will find that the [`Object`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object) type is full of handy built-in methods to make creating object easier.

There's not much you can do about having to construct objects from scratch, but if the data for an object is contained in another format (say an array or a map read from an external source), then you can use `Object.fromEntries`. Perhaps you are reading a formatted csv-type file and you are given a header row and data row. To create an object, simply do:

```
var headers = ['a', 'b', 'c', 'd']
var data = [1, 2, 3, 4]
var obj = Object.fromEntries(headers.map((val, idx) => [val, data[idx]]))
// Object { a: 10, b: 11, c: 12, d: 13 }
```

(Yes you do need to know what `Array.map` does, more on that later)

What about if you have an array of objects, and you want to create a fast lookup of two related fields, say a shipment ID to an address?

```
// data = array of objects with fields { id, name, price, address, description... }
var myMapObj = Object.fromEntries(data.map(item => [item.id, item.description]))
```

_If you don't know what this is good for, if you need to look up an address for an ID many times, then searching the original `data` array over and over is going to be hugely inefficient. Making one object allows you do do an operation like `myMapObj[id]` in O(1) time, so after only a few lookups, despite having to create the map, your code becomes very fast._

The other Object method to consider is [`Object.assign`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign). This copies one or more source objects into a target object (and modifies the target object - be aware of this). This is obviously useful when merging two objects into one, and also for overriding things in an existing object.

Perhaps you want to assign user-overrides onto a default structure. In the old days perhaps you checked and copied every custom item? Instead you can use Object.assign:

```
var defaultObj = {
    Name: 'myObj',
    priority: 'NORMAL',
    colour: 'blue',
    deliverDate: new Date().toISOString().split('T')[0]
}
var userOptions = { priority: 'HIGH', colour: 'red' }
var orderObj = Object.assign({}, defaultObj, userOptions)
```

Perhaps you have information from different sources which you want to combine:

```
// Continue from above, item and address information from different sources
Object.assign(orderObj, itemData, {pickup: pickupData}, {dropoff: dropoffData})
```

Those of you in the know will notice that if you are making a *new* object, you can just use the spread operator (`...`), which is a bit more readable:

```
var shipmentObj = {
    ...defaultObj,
    ...userOptions,
    ...itemData,
    pickup: pickupData,
    dropoff: dropoffData
}
```

The key difference as mentioned before is that `Object.assign` lets you modify the target object. So if the target object is `{}`, then the behaviour is the same as using spreads. If it is an existing object then it can be modified in bulk. These two methods can also be combined in many cases very elegantly.

![Mind Blown](images/mind_blown.jpg)

## Advanced Stuff

### Dynamic Object Manipulation

Now on to the good stuff. Sometimes you want to make an object with fields that may depend on run-time conditions. Say you deal with object formats that carry almost identical information just with different fields names. A slightly corny example is transaction accounts:

```
// Sender account
var sender = {
    transactionType: "SEND",
    senderName: ...,
    senderAccount: ...,
    amount: ...
}

// receiver account
var receiver = {
    transactionType: "RECV",
    receiverName: ...,
    receiverAccount: ...,
    amount: ...
}
```

This may be corny, but depending on who wrote your models this can happen. Think postal sender & receiver, goods sender & receiver or in-game transactions. Perhaps they are two separate systems talking to each other.

Anyway, one upon a time I had to do this:

```
if (obj.transactionType == "SEND") {
    obj['senderName'] = "Phil"
    obj['senderAccount'] = 12345
}
else if (obj.transactionType == "RECV") {
    // You get the picture
}
```

Then I discovered that JavaScript supports dynamic field names, allowing this:

```
var [nameField, accountField] = obj.transactionType == "SEND" ? ['senderName', 'senderAccount'] : ['receiverName', 'receiverAccount']
Object.assign(obj,
    {
        [nameField]: "Phil",
        [accountField]: 12345
    }
)
```

This syntax accepts expressions, so you can even do this:

```
var prefix = obj.transactionType == "SEND" ? "sender" : "receiver"
Object.assign(obj,
    {
        [prefix + "Name"]: "Phil",
        [prefix + "Account"]: 12345
    }
)
```

Nice.

The other thing I struggled with is when you may or may not require a field based on some run-type context or condition. I didn't really want to do this over and over again:

```
if (condition == 1) {
    obj['someField'] = 'yes'
}
```

You can put conditions into the filed definition, but then you will end up with NULL fields, which may affect other logic:
```
var obj = {
    // other fields...
    'someField': condition ? 'yes' : null
}
```

If you have been paying attention, you can use `Object.assign`:

```
Object.assign(obj, condition ? { someField: 'yes' } : {})
```

This works great if a whole sub-set of fields is conditional on the same thing, but what about if each field is different?

Well, this may not be a built-in feature but it is a neat trick. Here is an example of including a date in an object only if requested:

```
var obj = {
    // Other stuff
    ...(includeDate && {when: moment(momentString, "YYYY-MM-DD hh:mm A").toISOString()})
}
```

The cool thing here is if `includeData` evaluates to false, the spread operator operates on nothing but it is a legal syntax. If it evaluates to true, it operates on the object. This has been a great saver for me.

### Getting Funky-tional

Welcome to the home of bad puns, but great tips.

My opinion is that these days, especially since so many languages provide these features built-in, every developer must know the three key functional transformers: map, filter and reduce. Most of the code that we write handles lists of data and processes or transforms it, so these functions come up time and time again.

JavaScript has had these functions built in for a while now. It is not really up to me to describe what they do - they are all listed on the [Mozilla Developer Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array) page.

What I can advise is that you stop using loops and start using these:

```
// Filter on all customers with outstanding invoices
var output = customers.filter(cust => cust.unpaid)

// Map customer email addresses
var addresses = customers.map(cust => cust.email)

// Get all emails of customers with unpaid invoices
var addresses = customers.filter(cust => cust.unpaid).map(cust => cust.email)
```

The fun starts when you know how to use reduce:
```
// For a customer, get their total outstanding invoice amount
var totalOutsanding = customer.invoices.filter(inv => inv.unpaid).reduce((tot, inv) => tot + inv.amount, 0)
```

Now, isn't that simpler than writing a big for-loop?

With great power comes great responsibility, as always, and as you master these function you will be faced with many ways that `map`, `filter` and `reduce` can be combined to get a desired output. _Not all of these will be optimally executable or readable_, and you will probably need to trade something off for readability. After all, many a great programmer has pointed out that while code is written once by one person, it is read many times by many other people. So clarity is key.

Think about how you would go through a big set of accounts data (e.g. multiple arrays of objects) to extract the information required to send emails to all customers with outstanding account, including the amount details and the total. Could this be a filter and a map? Or a filter and a reduce? Or a filter with a reduce inside a map? Or is there another way of doing this? I recommend that you should use these functions as much as you can, but not to the point of obfuscating your code.

### Functions First

Related to the above section is to remind you that, as with all great languages, functions are treated as first-class citizens in Javascript. This means that you can pass functions into other functions, such as creating your own functions to pass into the `map` and `filter` functions above.

Say you have an import function which knows how to report progress. Your import function is used by two different web pages each with their own progress bar implementation. This doesn't matter - your import function can offer to accept a progress function _as long as the interface is the same_. That is to say that as long as the progress function takes an integer between 0 and 100, it can be accepted by your import function.

```
def myImportFunction(data, progressFcn = null) {
    while (doStuffWith(data)) {

        if (progressFcn) {
            progressFcn(updateValue)
        }
    }
}
```

The other great thing about first-class functions is they can be passed around like anything else. A further example of the import function is that you can define a list of steps, which are functions to be called:

```
def myImportFunction(data, progressFcn = null) {

    var processSteps = [
        validateFcn,
        readFcn,
        transformFcn,
        formatFcn
    ]

    //Use our magical reduce function
    return processSteps.reduce((acc, stage) => stage(acc), data)
}
```

With the magic of `reduce`, this will take our `data` for processing, and will chain the output from each function to the next in the list. Doing this makes for a nice readable function (you can see the order of the process steps nice and clearly), and also means you can test your process functions individually (read more about this in [my Pipeline post](./2022-07-20-software-pipelines.markdown))

