# executorlib-core
The `executorlib-core` package is based on the [concurrent.futures.Executor](https://docs.python.org/3/library/concurrent.futures.html)
abstract class from the Python standard library to define `Executor` classes for specific application. This is achieved
by coupling two Python processes using [zeroMQ](https://zeromq.org) universal messaging library and serializing the 
Python objects using [cloudpickle](https://github.com/cloudpipe/cloudpickle) which extends the serialization support for
Python objects. 