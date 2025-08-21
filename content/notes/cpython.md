---
title: "cPython"
date: 2025-08-15
tags: [programming, python]
draft: true
---

## Moving pieces

Starting in python 3.12, garbage collection can only occur in `eval breaker`

https://github.com/python/cpython/issues/97922


## How does eval breaker work?
*In the latest Python...*

In `Include/internal/pycore_ceval.h`

We find:

```
/* Bits that can be set in PyThreadState.eval_breaker */
#define _PY_GIL_DROP_REQUEST_BIT (1U << 0)
#define _PY_SIGNALS_PENDING_BIT (1U << 1)
#define _PY_CALLS_TO_DO_BIT (1U << 2)
#define _PY_ASYNC_EXCEPTION_BIT (1U << 3)
#define _PY_GC_SCHEDULED_BIT (1U << 4)
#define _PY_EVAL_PLEASE_STOP_BIT (1U << 5)
#define _PY_EVAL_EXPLICIT_MERGE_BIT (1U << 6)
#define _PY_EVAL_JIT_INVALIDATE_COLD_BIT (1U << 7)
```

These bits are the bits that can be set in order to stop execution of a PyThread, in order to do any of the above.

### GC / Eval Breaker

We find this function which schedules gc

```
void
_PyObject_GC_Link(PyObject *op)
{
    PyGC_Head *gc = AS_GC(op);
    // gc must be correctly aligned
    _PyObject_ASSERT(op, ((uintptr_t)gc & (sizeof(uintptr_t)-1)) == 0);

    PyThreadState *tstate = _PyThreadState_GET();
    GCState *gcstate = &tstate->interp->gc;
    gc->_gc_next = 0;
    gc->_gc_prev = 0;
    gcstate->young.count++; /* number of allocated GC objects */
    gcstate->heap_size++;
    if (gcstate->young.count > gcstate->young.threshold &&
        gcstate->enabled &&
        gcstate->young.threshold &&
        !_Py_atomic_load_int_relaxed(&gcstate->collecting) &&
        !_PyErr_Occurred(tstate))
    {
        _Py_ScheduleGC(tstate);
    }
}
```


_Note: I am ignoring all freethreading..._
This is the only function that calls `_Py_ScheduleGC`.

The only function that calls `_PyObject_GC_Link` is:

```
static PyObject *
gc_alloc(PyTypeObject *tp, size_t basicsize, size_t presize)
{
    PyThreadState *tstate = _PyThreadState_GET();
    if (basicsize > PY_SSIZE_T_MAX - presize) {
        return _PyErr_NoMemory(tstate);
    }
    size_t size = presize + basicsize;
    char *mem = _PyObject_MallocWithType(tp, size);
    if (mem == NULL) {
        return _PyErr_NoMemory(tstate);
    }
    ((PyObject **)mem)[0] = NULL;
    ((PyObject **)mem)[1] = NULL;
    PyObject *op = (PyObject *)(mem + presize);
    _PyObject_GC_Link(op);
    return op;
}
```

In other words, once we make enough objects, we will _schedule_ GC.

## When are the eval breaker bits set?

... depends on which python version you're using ...
... oh man... Let's start over.
In `Python 3.13+`...
TODO

In `python 3.11.9`...


# In Python 3.11.9...

In Python 3.11.9, the `eval breaker` is a single atomic integer, stored in the _interpreter state_.

The `GC` system does not depend on `eval_breaker`, it is just called once enough objects are called.

```
void
_PyObject_GC_Link(PyObject *op)
{
    PyGC_Head *g = AS_GC(op);
    assert(((uintptr_t)g & (sizeof(uintptr_t)-1)) == 0);  // g must be correctly aligned

    PyThreadState *tstate = _PyThreadState_GET();
    GCState *gcstate = &tstate->interp->gc;
    g->_gc_next = 0;
    g->_gc_prev = 0;
    gcstate->generations[0].count++; /* number of allocated GC objects */
    if (gcstate->generations[0].count > gcstate->generations[0].threshold &&
        gcstate->enabled &&
        gcstate->generations[0].threshold &&
        !gcstate->collecting &&
        !_PyErr_Occurred(tstate))
    {
        gcstate->collecting = 1;
        gc_collect_generations(tstate);
        gcstate->collecting = 0;
    }
}
```
This behavior was changed here:
https://github.com/python/cpython/issues/97922

Seems like a very reasonable thing to do.


# Hilarious things I've found:

https://github.com/pablogsal/python-horror-show

# GC:

Each call to GC may not actually GC:

```
static Py_ssize_t
gc_collect_generations(PyThreadState *tstate)
{
    GCState *gcstate = &tstate->interp->gc;
    /* Find the oldest generation (highest numbered) where the count
     * exceeds the threshold.  Objects in the that generation and
     * generations younger than it will be collected. */
    Py_ssize_t n = 0;
    for (int i = NUM_GENERATIONS-1; i >= 0; i--) {
        if (gcstate->generations[i].count > gcstate->generations[i].threshold) {
            /* Avoid quadratic performance degradation in number
               of tracked objects (see also issue #4074):

               To limit the cost of garbage collection, there are two strategies;
                 - make each collection faster, e.g. by scanning fewer objects
                 - do less collections
               This heuristic is about the latter strategy.

               In addition to the various configurable thresholds, we only trigger a
               full collection if the ratio

                long_lived_pending / long_lived_total

               is above a given value (hardwired to 25%).

               The reason is that, while "non-full" collections (i.e., collections of
               the young and middle generations) will always examine roughly the same
               number of objects -- determined by the aforementioned thresholds --,
               the cost of a full collection is proportional to the total number of
               long-lived objects, which is virtually unbounded.

               Indeed, it has been remarked that doing a full collection every
               <constant number> of object creations entails a dramatic performance
               degradation in workloads which consist in creating and storing lots of
               long-lived objects (e.g. building a large list of GC-tracked objects would
               show quadratic performance, instead of linear as expected: see issue #4074).

               Using the above ratio, instead, yields amortized linear performance in
               the total number of objects (the effect of which can be summarized
               thusly: "each full garbage collection is more and more costly as the
               number of objects grows, but we do fewer and fewer of them").

               This heuristic was suggested by Martin von Löwis on python-dev in
               June 2008. His original analysis and proposal can be found at:
               http://mail.python.org/pipermail/python-dev/2008-June/080579.html
            */
            if (i == NUM_GENERATIONS - 1
                && gcstate->long_lived_pending < gcstate->long_lived_total / 4)
                continue;
            n = gc_collect_with_callback(tstate, i);
            break;
        }
    }
    return n;
}
```