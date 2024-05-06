from concurrent.futures import (
    Executor as FutureExecutor,
    Future,
)
import inspect
import queue
from typing import List

import cloudpickle

from executorlib_core.thread import RaisingThread
from executorlib_core.inputcheck import (
    check_resource_dict,
    check_resource_dict_is_empty,
)


class ExecutorBase(FutureExecutor):
    def __init__(self):
        cloudpickle_register(ind=3)
        self._future_queue = queue.Queue()
        self._process = None

    @property
    def info(self):
        if self._process is not None and isinstance(self._process, list):
            meta_data_dict = self._process[0]._kwargs.copy()
            if "future_queue" in meta_data_dict.keys():
                del meta_data_dict["future_queue"]
            meta_data_dict["max_workers"] = len(self._process)
            return meta_data_dict
        elif self._process is not None:
            meta_data_dict = self._process._kwargs.copy()
            if "future_queue" in meta_data_dict.keys():
                del meta_data_dict["future_queue"]
            return meta_data_dict
        else:
            return None

    @property
    def future_queue(self):
        return self._future_queue

    def submit(self, fn: callable, *args, resource_dict: dict = {}, **kwargs):
        """
        Submits a callable to be executed with the given arguments.

        Schedules the callable to be executed as fn(*args, **kwargs) and returns
        a Future instance representing the execution of the callable.

        Args:
            fn (callable): function to submit for execution
            args: arguments for the submitted function
            kwargs: keyword arguments for the submitted function
            resource_dict (dict): resource dictionary, which defines the resources used for the execution of the
                                  function. Example resource dictionary: {
                                      cores: 1,
                                      threads_per_core: 1,
                                      gpus_per_worker: 0,
                                      oversubscribe: False,
                                      cwd: None,
                                      executor: None,
                                      hostname_localhost: False,
                                  }

        Returns:
            A Future representing the given call.
        """
        check_resource_dict_is_empty(resource_dict=resource_dict)
        check_resource_dict(function=fn)
        f = Future()
        self._future_queue.put({"fn": fn, "args": args, "kwargs": kwargs, "future": f})
        return f

    def shutdown(self, wait: bool = True, *, cancel_futures: bool = False):
        """
        Clean-up the resources associated with the Executor.

        It is safe to call this method several times. Otherwise, no other
        methods can be called after this one.

        Args:
            wait: If True then shutdown will not return until all running
                futures have finished executing and the resources used by the
                parallel_executors have been reclaimed.
            cancel_futures: If True then shutdown will cancel all pending
                futures. Futures that are completed or running will not be
                cancelled.
        """
        if cancel_futures:
            cancel_items_in_queue(que=self._future_queue)
        self._future_queue.put({"shutdown": True, "wait": wait})
        if wait and self._process is not None:
            self._process.join()
            self._future_queue.join()
        self._process = None
        self._future_queue = None

    def _set_process(self, process: RaisingThread):
        self._process = process
        self._process.start()

    def __len__(self):
        return self._future_queue.qsize()

    def __del__(self):
        try:
            self.shutdown(wait=False)
        except (AttributeError, RuntimeError):
            pass


class ExecutorBroker(ExecutorBase):
    def shutdown(self, wait: bool = True, *, cancel_futures: bool = False):
        """Clean-up the resources associated with the Executor.

        It is safe to call this method several times. Otherwise, no other
        methods can be called after this one.

        Args:
            wait: If True then shutdown will not return until all running
                futures have finished executing and the resources used by the
                parallel_executors have been reclaimed.
            cancel_futures: If True then shutdown will cancel all pending
                futures. Futures that are completed or running will not be
                cancelled.
        """
        if cancel_futures:
            cancel_items_in_queue(que=self._future_queue)
        if self._process is not None:
            for _ in range(len(self._process)):
                self._future_queue.put({"shutdown": True, "wait": wait})
            if wait:
                for process in self._process:
                    process.join()
                self._future_queue.join()
        self._process = None
        self._future_queue = None

    def _set_process(self, process: List[RaisingThread]):
        self._process = process
        for process in self._process:
            process.start()


def cancel_items_in_queue(que: queue.Queue):
    """
    Cancel items which are still waiting in the queue. If the executor is busy tasks remain in the queue, so the future
    objects have to be cancelled when the executor shuts down.

    Args:
        que (queue.Queue): Queue with task objects which should be executed
    """
    while True:
        try:
            item = que.get_nowait()
            if isinstance(item, dict) and "future" in item.keys():
                item["future"].cancel()
                que.task_done()
        except queue.Empty:
            break


def cloudpickle_register(ind: int = 2):
    """
    Cloudpickle can either pickle by value or pickle by reference. The functions which are communicated have to
    be pickled by value rather than by reference, so the module which calls the map function is pickled by value.
    https://github.com/cloudpipe/cloudpickle#overriding-pickles-serialization-mechanism-for-importable-constructs
    inspect can help to find the module which is calling pympipool
    https://docs.python.org/3/library/inspect.html
    to learn more about inspect another good read is:
    http://pymotw.com/2/inspect/index.html#module-inspect
    1 refers to 1 level higher than the map function

    Args:
        ind (int): index of the level at which pickle by value starts while for the rest pickle by reference is used
    """
    try:  # When executed in a jupyter notebook this can cause a ValueError - in this case we just ignore it.
        cloudpickle.register_pickle_by_value(inspect.getmodule(inspect.stack()[ind][0]))
    except IndexError:
        cloudpickle_register(ind=ind - 1)
    except ValueError:
        pass
