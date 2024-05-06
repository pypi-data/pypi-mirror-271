# Simulation experiment with needles

## Blogpost
Please consider to also read my blogpost on [Medium](https://medium.com/@ma.draws/simulation-experiment-with-needles-c4a5dbf5f3e1).

## Authors and Licensing
- Author: Martin Draws

- License [MIT License](https://opensource.org/license/mit)

## Motivation
The problem discussed here might seem random. But the aim of this package is to show that an apparently complex challenge can be broken down into mathematical expressions to answer a certain question.

# Task
Imagine the following situation. You have a table with parallel lines on it. The distance between these lines is constant across the table.

And you have a needle. It can be any kind of needle, but if it makes things easier for you, just imagine the needle is a sewing needle. The needle has a certain length.

We would like to answer the following question: given the distance between the parallel lines on the table and the needle's length, what is the likelihood that the needle crosses a line on the table after it fell on it?

## Installation
To install the package from PyPi yout have to execute the following.

```
python -m pip install drop-needle 
```

## Functionality
After installation the package can be loaded.

````
from drop_needle.Table import Table

# Initialize a table with a distance of 10 between the lines
table = Table(10)

# Simulate 10,000 needles with a length of 7 falling on the table
table.simulate(10000, 7)
0.4401
````
