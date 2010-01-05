"""
This file contains an implementation of a finite state automaton,
using generator functions as coroutines.
"""

import functools
import time
import warnings

__all__ = ('Coroutine', 'Case', 'State', 'FSA', 'coroutine', 'state', 'fsa',
           'FSA_INPUT', 'FSA_YIELD', 'FSA_PUSH', 'FSA_POP', 'FSA_SWAP')

##
# Helper factory functions
##

def meta_decorator_factory(meta_target):
    '''Generate a decorator that optionally accepts keyword arguments
    before being called with a target function.'''
    def meta_decorator(target=None, **kwargs):
        def decorator(target):
            return meta_target(target, **kwargs)
        if target is None:
            return decorator
        return meta_target(target, **kwargs)
    return meta_decorator


##
# Wrapper class for generators that implement coroutines.
##

class Coroutine(object):
    '''Coroutine generator function wrapper class.'''
    def __init__(self, target=None, name=None, doc=None):
        if target is not None:
            self.run = target
            if name is None:
                name = target.__name__
            if doc is None:
                doc = target.__doc__
        self.__name__ = name
        self.__doc__ = doc

    def __call__(self, *args, **kwargs):
        '''Return a running coroutine instance.'''
        if self.send != self._send:
            raise TypeError("%r already started" % self)
        gen = self.run(*args, **kwargs)
        if not isinstance(self.run, Coroutine):
            gen.next()
        cr = self.clone()
        # disable calling run()
        cr.run = self._run_started
        # enable calling send()
        cr.send = gen.send
        return cr

    def _run(self, *args, **kwargs):
        raise NotImplementedError("no target specified for coroutine %r" %
                                  self)
    run = _run

    def _run_started(self, *args, **kwargs):
        raise TypeError("Coroutine called while running", self)
    
    def _send(self, arg):
        raise TypeError("Coroutine sent value before start", self)
    send = _send

    def clone(self):
        return Coroutine(target=self.run, name=self.__name__, doc=self.__doc__)

    def __eq__(self, other):
        return isinstance(other, Coroutine) and self.run == other.run

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.__name__)

coroutine = meta_decorator_factory(Coroutine)


##
# Coroutine-based state decorator
##

class State(Coroutine):
    '''Implements a series of states in a finite state automaton.

    A class with a run() method that is a generator may extend fsa.State,
    which implements __call__().  Alternatively, any generator function
    may be decorated with the fsa.state (lowercase) decorator, which
    returns a State instance with run() replaced.  In either case, the
    generator method is wrapped by fsa.Coroutine.  Note that all
    generator functions must contain at least one yield statement and no
    return statement.  Unlike a normal generator, an fsa.Coroutine will
    execute up to the first yield statement when first called.

    Examples:
    
    @fsa.state
    def foo(self):
        """The foo state"""
        yield

    @fsa.state(name='Hello World', doc='say hello')
    def hello_world(self):
        yield
        print 'Hello World!'

    class Bar(State):
        """Serve a drink"""
        def run(self):
            customer = yield
            if 'soda' in customer.request:
                yield 'Coke'
            if customer.age >= 21:
                yield 'Jack'

    The fsa.State decorator will pass an instance of itself as the first
    argument to decorated functions (extending classes receive this
    argument naturally).  Any initialization code may be run before the
    first yield statement.   From then on, the code between each yield
    statement runs in a single frame of execution.  As a coroutine, input
    may be drawn from each yield statement.
    '''
    def __init__(self, target=None, name=None, doc=None, _dowrap=True,
                 **states):
        if target is not None:
            if name is None:
                name = target.__name__
            if doc is None:
                doc = target.__doc__
            if _dowrap:
                target = functools.partial(target, self)
        else:
            target = self.run
            if name is None:
                name = self.__class__.__name__
            if doc is None:
                doc = self.__class__.__doc__
        super(State, self).__init__(target=target, name=name, doc=doc)
        # record instance-specific states
        self.states = states
        for name, state in self.states.iteritems():
            if hasattr(self, name):
                raise NameError("Reserved attribute '%s'" % name)
            setattr(self, name, state)

    def case(self, *args, **kwargs):
        return Case(self, *args, **kwargs)

    def clone(self):
        return State(target=self.run, name=self.__name__, doc=self.__doc__,
                    _dowrap=False, **self.states)

    def partial(self, *args, **kwargs):
        state = self.clone()
        state.run = functools.partial(state.run, *args, **kwargs)
        return state

    def statedict(self):
        # copy keyword states
        d = dict(self.states)
        func = self._get_func()
        if hasattr(func, 'func_code') and hasattr(func, 'func_globals'):
            # introspect code to find referenced global states & coroutines
            for name in func.func_code.co_names:
                val = func.func_globals.get(name)
                if isinstance(val, State):
                    d[name] = val
        return d

    def _get_func(self):
        func = self.run
        while hasattr(func, 'func'):
            func = func.func
        return func

state = meta_decorator_factory(State)


## 
# Case-specific states
##

def always(input):
    '''Always true'''
    return True

class Case(State):
    '''An fsa.State that includes a test case function.'''
    def __init__(self, state=state, when=always, reason=''):
        self.when = when
        self.reason = reason
        super(Case, self).__init__(target=state.run, name=state.__name__,
                doc=state.__doc__, _dowrap=False, **state.states)
    
    def check(self, input):
        return self.when(input)

    def enter(self, *args, **kwargs):
        return FSA_PUSH, self(*args, **kwargs)

    def enterLater(self, *args, **kwargs):
        return FSA_PUSH | FSA_YIELD, self(*args, **kwargs)

    def enter_or_yield(self, input, *args, **kwargs):
        if self.check(input):
            return FSA_PUSH, self(*args, **kwargs)
        return FSA_YIELD, None

    def enter_or_None(self, input, *args, **kwargs):
        if self.check(input):
            return FSA_PUSH, self(*args, **kwargs)

    def clone(self):
        return Case(state=self, when=self.when, reason=self.reason)


##
# FSA implementation
##

# action bitmasks
FSA_INPUT = 0
FSA_YIELD = 1
FSA_PUSH = 2
FSA_POP = 4
FSA_SWAP = 6

class FSA(State):
    '''Finite State Automaton implementation using coroutines.
    
    Implements a core run() method, plus several helper functions that
    mimic the previous FSA API.  Each call to step() sends an input into
    the running FSA.  If an input function is provided it will be called
    with no arguments each frame.  Otherwise, step() will pass the FSA
    itself as input.
    '''
    def __init__(self, initial=None, input=None, name=None, doc=None):
        super(FSA, self).__init__(name=name, doc=doc)
        self.initial = initial
        self.input = input

    def step(self):
        input = self
        if self.input:
            input = self.input()
        try:
            self.send((FSA_INPUT, input))
        except StopIteration:
            warnings.warn(RuntimeWarning(self, 'iteration has ended'))

    def run(self, verbose=False, debug=False):
        '''A coroutine implementation of a finite state automaton.

        Implements a frame-based finite state automaton with runtime control
        over flow of execution.  Each frame, a tuple of the form
        (action, value) is expected as input to control the operation on a
        stack of sub-state coroutines.  When coroutines in the stack are
        executed, they are expected to yield tuples in the same format. The
        stack may be initially filled through the 'states' argument. 
    
        For the (action, value) tuple, the value field depends on the action.
        The action may be a bit-wise OR of one or more of the following:
    
            FSA_INPUT
                The value is an input value to be sent to the coroutine at
                the top of the stack.  Execution will continue to follow the
                orders of the child coroutine until it yields via
                FSA_YIELD.  As this is expected to be used only externally,
                the bit mask is 0 and will only be executed if none of the
                following flags are specified.
    
            FSA_YIELD
                No value is required (default None). Implies the frame is
                finished and the FSA should itself yield value to wait for
                the next input.  Use of this from outside of a child
                coroutine will accomplish very little.  When yielding from
                within a child coroutine, without specifying FSA_YIELD the
                fsa will continue immediately to execute the coroutine at the
                head of the stack, often the same one which just yielded.
                FSA.clean() sets this flag automatically when no flags have
                been returned explicitly.  When combined with any of the
                following flags, the requested actions will occur before the
                FSA yields.
    
            FSA_PUSH
                The value is an fsa.Coroutine instance that the FSA should
                push onto the head of the stack.

            FSA_POP
                No value is required.  Pops a coroutine from the stack.
    
            FSA_SWAP
                The value is an fsa.Coroutine instance that the FSA should
                push onto the head of the stack, after first popping the
                current head.  FSA_SWAP is the bitwise OR of FSA_PUSH and
                FSA_POP.
        '''
        action = input = value = None
        # initialize state stack
        stack = []
        if self.initial:
            stack.append(self.initial)
        # wait for initial action tuple
        action, input = yield
        start_time = time.time()
        while True:
            if debug:
                print "DEBUG: %s - (%i, %s)" % (self.__name__, action, value)
            # process action
            if action & FSA_POP:
                action ^= FSA_POP
                if not stack:
                    break
                stack.pop()
            if action & FSA_PUSH:
                action ^= FSA_PUSH
                stack.append(value)
            if action & FSA_YIELD:
                # wait for next input
                if verbose:
                    print 'FSA frame completed in ', time.time() - start_time
                action, input = yield value
                start_time = time.time()
            elif action == FSA_INPUT:
                # retrieve head of stack
                if not stack:
                    break
                state = stack[-1]
                # send input to coroutine
                try:
                    action, value = state.send(input)
                except StopIteration:
                    if not stack:
                        raise
                    action = FSA_YIELD | FSA_POP
            else:
                raise ValueError("unknown flag %i" % action)

    def clean(self, cr, result):
        '''Parse an action tuple yielded by this state'''
        if not isinstance(result, tuple):
            if hasattr(result, '__iter__'):
                result = tuple(result)
            else:
                result = (result,)
        if len(result) == 2:
            return result
        elif len(result) == 1:
            if isinstance(result[0], int):
                return result[0], cr
            else:
                return FSA_YIELD, result[0]
        return FSA_YIELD, cr

    def clone(self):
        return self.__class__(initial=self.initial, input=self.input,
                              name=self.__name__, doc=self.__doc__)

    def statedict(self):
        return {'initial': self.initial}

    # simulate former FSA API
    @staticmethod
    def stay(value=None):
        ''' --> (int, coroutine).  Helper to generate (FSA_YIELD, value)
        coroutine action tuple.

        Yield the result of this method to stay in this state coroutine
        but wait for the next vision frame.
        '''
        return FSA_YIELD, value

    @staticmethod
    def goNow(state):
        ''' --> (int, coroutine).  Helper to generate (FSA_SWAP, state)
        coroutine action tuple.
        
        Use this method to switch to a new state immediately.'''
        return FSA_SWAP, state

    @staticmethod
    def goLater(state):
        ''' --> (int, coroutine).  Helper to generate
        (FSA_SWAP | FSA_YIELD, state) coroutine action tuple.

        Use this method to switch to a new state and wait for a new vision
        frame.
        '''
        return FSA_SWAP | FSA_YIELD, state
    
    def switchTo(self, state):
        '''Method used to change the state from outside the FSA_'''
        self.send((FSA_SWAP | FSA_YIELD, state))

def fsa(target=None, verbose=False, debug=False, FSA=FSA):
    '''Decorate a function with an fsa.FSA instance.

    If the function isn't supplied initially, act as a meta deocrator and
    return another decorator expecting the function.'''
    if target is None:
        def meta_decorator(final_target):
            f = FSA(target.__name__, target.__doc__)
            return f([target], verbose, debug)
        return meta_decorator
    f = FSA(target.__name__, target.__doc__)
    return f([target], verbose, debug)


TABWIDTH = 4
def print_tree(state, indent=0):
    if indent:
        if indent > TABWIDTH:
            print (' ' * TABWIDTH + '-' * (indent - TABWIDTH - 1) + '>' +
                    repr(state))
        else:
            print ('-' * (indent - 1) + '>' + repr(state))
    else:
        print repr(state)
    prefix = ' ' * indent
    print prefix + '  ' + state.__doc__
    if hasattr(state, 'reason'):
        print prefix + 'reason: ' + state.reason
    print

    substates = state.statedict()
    for name in sorted(substates):
        print prefix + "substate '%s'" % name
        print_tree(substates[name], indent + TABWIDTH)
    


##
# Simple test example
##

if __name__ == '__main__':
    import sys

    @state
    def hello(self, suffix='.'):
        '''Say hello, and exit'''
        input = yield
        print 'Hello %s%s' % (input, suffix)

    def always(input):
        '''Always true'''
        return True
    
    @state(
        name='Cheerful Greeter',
        doc='Greet every input with a cheerful hello!',
        hello=hello.case(when=always, reason='always'),
    )
    def greeter(self):
        input = yield
        while True:
            # Check our private 'hello' case of the 'hello' state
            if self.hello.check(input):
                # say hello to our friend
                input = yield self.hello.enter('!')
                # when hello() raises StopIteration, the FSA will yield
                # when next called, the FSA will re-enter here
            else:
                raise NotImplementedError("shouldn't reach here")

    # An alternative implementation
    @state(
        friend = hello.partial('!').case(
            when=lambda (friends, person): person in friends,
            reason='is a friend'
        ),
        other = hello.case(when=always, reason='otherwise')
    )
    def friend_greeter(self, friends):
        '''Greet my friends warmly.'''
        def run(self, friends):
            input = yield
            while True:
                case_input = friends, input
                input = yield (
                    self.friend.enter_or_None(case_input) or
                    self.other.enter_or_yield(case_input)
                    )

    # Create a new FSA
    RawNameInputFSA = FSA(
        initial=friend_greeter.partial(['Billy', 'Joanna']),
        input=functools.partial(raw_input, 'Enter your name: '),
        name='RawNameInputFSA',
        doc='read from stdin'
        )
    # Run the FSA
    fsa = RawNameInputFSA(debug='-d' in sys.argv[1:])
    print_tree(fsa)
    try:
        while True:
            fsa.step()
    except (KeyboardInterrupt, EOFError):
        print '\nGoodbye!'

