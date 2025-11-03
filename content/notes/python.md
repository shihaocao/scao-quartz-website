---
title: "Python..."
date: 2025-02-28
tags: [code]
---

## Typically I'm a fan of Python, but...

Python integers are infinite precision, great!
But working with binary math + negative numbers can be confusing.
- https://stackoverflow.com/questions/46993519/python-representation-of-negative-integers

Essentially, assume Python stores negative numbers also with infinite precision but in two's compliment when doing binary math.

---

A favorite: Python Horror Show:

https://github.com/pablogsal/python-horror-show


---

Since python 3.10, Python supports the `bit_count()`

https://docs.python.org/3.10/library/stdtypes.html#:~:text=in%20version%203.1.-,int.bit_count()%C2%B6,-Return%20the%20number


https://faun.pub/why-dict-vs-slots-in-python-is-very-important-a271fbfd08db

https://docs.python.org/3/library/dataclasses.html#:~:text=slots%3A%20If%20true%20(the%20default%20is%20False)%2C%20__slots__%20attribute%20will%20be%20generated%20and%20new%20class%20will%20be%20returned%20instead%20of%20the%20original%20one.%20If%20__slots__%20is%20already%20defined%20in%20the%20class%2C%20then%20TypeError%20is%20raised.

