---
title: "Small String Optimization"
date: 2022-07-02
tags: [code]
---

TLDR:
One day, I was like, oh! I can just use std::string as a return because SSO will take place, but then immediately I was like, but SSO still won't be as fast as a `const char *`

So I wanted to see what the actual difference was.

Links:
- https://stackoverflow.com/questions/10315041/meaning-of-acronym-sso-in-the-context-of-stdstring/10319672#10319672
- https://stackoverflow.com/questions/21694302/what-are-the-mechanics-of-short-string-optimization-in-libc

When are temporary objects destroyed?
- https://stackoverflow.com/questions/2298781/when-are-temporary-objects-destroyed
- https://eel.is/c++draft/intro.execution#def:full-expression

Quick Bench:
- https://quick-bench.com/

![Quick Bench](notes/images/sso/quick-bench.jpg)

God Bolt Comparison
- https://godbolt.org/z/a3zhjKn33
![God Bolt](notes/images/sso/god-bolt.jpg)