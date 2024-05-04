"""This file contains higher interface evaluators that allow parallel runs and callbacks in the main thread.
They are used in two places: Sensitivity analyses and Optimization
Usage:
-> initialize with "settings" as argument
-> use set_evaluation_function(function, arguments_function)
-> use add_callback(callback_function) for a callback
-> use start before running the algorithm
-> use close to properly close the processes (if any)
When using evaluator.evaluate(job), the evaluator calls function(job, arguments_function(settings))
We call evaluator.callbacks(result)
and then return the result
The method evaluator.evaluate_all(jobs), then parallel run might be working (depending on the subclass of Evaluator).
"""
import _queue
import os

from optimeed.core.tools import printIfShown, SHOW_WARNING, AlwaysRaiseException
from optimeed.core.commonImport import SHOW_INFO
from multiprocessing import Pool, cpu_count, Process, Queue
from abc import ABC, abstractmethod


class AbstractEvaluator(ABC):
    def __init__(self, settings):
        self.settings = settings
        self.callbacks = set()
        self._evaluate = None
        self._get_evaluate_args = None
        self._default_return_values = None

    def set_evaluation_function(self, evaluate_function, get_evaluate_args):
        self._evaluate = evaluate_function
        self._get_evaluate_args = get_evaluate_args

    def set_default_returned_values(self, default_returned_values):
        """In case the evaluation fails, tell what to do"""
        self._default_return_values = default_returned_values

    def start(self):
        """Function that is called once just before starting the optimization"""
        pass

    def close(self):
        """Function that is called once after performing the optimization"""
        pass

    def do_callbacks(self, result_evaluation):
        """Perform the callbacks. Check `meth`:_evaluate for args"""
        for callback in self.callbacks:
            callback(result_evaluation)

    def add_callback(self, callback):
        """Add a callback method, to call everytime a point is evaluated"""
        self.callbacks.add(callback)

    @abstractmethod
    def evaluate(self, x):
        """Perform a single evaluation. Should slowly become deprecated (evaluate_all is more efficient)
        :param x: list of values [val1, val2, ..., valN] that are associated to the optimization parameters [1, 2, ..., N]
        :return output: output of :meth:`_evaluate`
        """
        pass

    @abstractmethod
    def evaluate_all(self, list_of_x):
        """Same as :meth:`AbstractEvaluator.evaluate`, but for a list of inputs (allow parallel run)
        :param list_of_x: list of args of :meth:`_evaluate`
        :return list of outputs of :meth:`_evaluate`
        """
        pass


class Evaluator(AbstractEvaluator):
    """Default evaluator that does not use parallel evaluations. => No risk of collision between concurrent threads. """
    def evaluate(self, x):
        results = self._evaluate(x, self._get_evaluate_args(self.settings))
        self.do_callbacks(results)
        return results

    def evaluate_all(self, list_of_x):
        return [self.evaluate(x) for x in list_of_x]


class MultiprocessEvaluator(Evaluator):
    """Allows multiprocess run. The arguments of _evaluate are NOT process safe: i.e. a new copy of
    characterization, objectives, constraints, device are copy at each call of :meth:`MultiprocessEvaluator.evaluate_all`
    In most of the cases it should be adequate, but this can be limiting if initialization of these classes is long.
    """
    def __init__(self, settings, number_of_cores=1):
        super().__init__(settings)
        self.pool = Pool(min(cpu_count(), number_of_cores))

    def evaluate_all(self, list_of_x):
        # There is a subtlety here: using multiprocess, both the args and the functions must be pickable
        # The function is pickled because on separate files => ok
        # Most of the optisettings are pickable, except the optialgorithm, that also references this class (MultiprocessEvaluator) => cannot be pickled
        # We, however, do not use it for the evaluation => use get_evaluate_args for those that need pickling.
        outputs = [self.pool.apply_async(self._evaluate, args=(x, self._get_evaluate_args(self.settings),), callback=self.do_callbacks) for x in list_of_x]
        return [output.get() for output in outputs]  # Same order as list_of_x => ok

    def close(self):
        printIfShown("Closing Pool", SHOW_INFO)
        self.pool.close()
        printIfShown("Waiting for all processes to complete", SHOW_INFO)
        self.pool.join()
        printIfShown("Pool closed", SHOW_INFO)


def _evaluate_with_queue(evaluate_function, evaluate_args, queue_evaluate, queue_results, default_returned_values):
    """Evaluate by the means of a queue. If a weird exception occurs => Put default values, update"""
    while True:
        index, x = queue_evaluate.get()
        if x == 'exit':  # Exit signal from queue
            break

        try:
            results_evaluation = evaluate_function(x, evaluate_args)
            queue_results.put((index, results_evaluation))
        except AlwaysRaiseException:  # The other are supposed to be managed within the evaluation function
            queue_results.put((index, default_returned_values(x, evaluate_args)))
            break


class _MyRestartingProcess:
    """Same as a process, but with a callback when abruptly killed"""

    def __init__(self, get_kwargs_process):
        self.continue_respawn = True
        self._get_kwargs_process = get_kwargs_process
        self.curr_process = None
        self.respawn()

    def start(self):
        self.curr_process.start()
        printIfShown("Process {} started !".format(hex(self.pid())), SHOW_INFO)

    def respawn(self):
        try:
            self.curr_process.kill()
        except AttributeError:
            pass
        del self.curr_process

        kwargs = self._get_kwargs_process()
        self.curr_process = Process(**kwargs)

    def is_alive(self):
        return self.curr_process.is_alive()

    def pid(self):
        return self.curr_process.pid

    def join(self):
        self.curr_process.join()


class PermanentMultiprocessEvaluator(AbstractEvaluator):
    """Allows multiprocess run. Conversely to :class:`MultiprocessEvaluator`, it uses a system of queue to send and gather results.
    The guarantees are the following: the arguments resulting of :meth:`get_evaluate_args` will be forked only once at the creation of the processes.
    Each process will be kept alive afterwards, and can reuse the same arguments
    => Useful when initializing the models generates a lot of overhead.
    """
    def __init__(self, settings, number_of_cores=1, timeout_check_processes=120):
        super().__init__(settings)
        self.all_processes = list()
        self.queue_evaluate = Queue()
        self.queue_results = Queue()
        self.number_of_cores = min(cpu_count(), number_of_cores)
        self.timeout_check_processes = timeout_check_processes

    def _get_kwargs_newprocess(self):
        kwargs_process = {'target': _evaluate_with_queue,
                          'args': (self._evaluate, self._get_evaluate_args(self.settings), self.queue_evaluate, self.queue_results, self._default_return_values,)}
        return kwargs_process

    def start(self):
        for i in range(self.number_of_cores):
            new_p = _MyRestartingProcess(self._get_kwargs_newprocess)
            new_p.start()
            self.all_processes.append(new_p)  # Keep them references

    def evaluate(self, x):
        self.queue_evaluate.put((0, x))
        return self.queue_results.get()

    def evaluate_all(self, list_of_x):
        for index, x in enumerate(list_of_x):
            self.queue_evaluate.put((index, x))

        num_to_complete = len(list_of_x)
        outputs = [None]*num_to_complete
        num_completed = 0
        while num_completed < num_to_complete:
            try:
                index, results = self.queue_results.get(timeout=self.timeout_check_processes)
                self.do_callbacks(results)
                outputs[index] = results
                num_completed += 1
            except _queue.Empty:
                printIfShown("Queue timed out ... Checking processes", SHOW_WARNING)
                # Check if needs respawns
                for process in self.all_processes:
                    if process.is_alive():
                        pass
                        # printIfShown("Process {} is alive".format(hex(process.pid())), SHOW_WARNING)
                    else:
                        printIfShown("Process {} is dead. Respawning a new process".format(hex(process.pid())), SHOW_WARNING)
                        process.respawn()
                        process.start()
        return outputs

    def close(self):
        printIfShown("Setting signals to stop processes", SHOW_INFO)

        for _ in range(len(self.all_processes)):
            self.queue_evaluate.put((0, 'exit'))

        printIfShown("Waiting for all processes to complete", SHOW_INFO)
        for p in self.all_processes:
            p.join()

        printIfShown("All processed have been successfully stopped", SHOW_INFO)

        self.queue_evaluate.close()
        self.queue_results.close()
