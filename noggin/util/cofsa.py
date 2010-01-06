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
        self.__running = False

    def __call__(self, *args, **kwargs):
        '''Return a running coroutine instance.'''
        if self.__running:
            raise TypeError("Coroutine called while running", self)
        gen = self.run(*args, **kwargs)
        if not isinstance(self.run, Coroutine):
            gen.next()
        cr = self.clone()
        cr.__running = True
        # enable calling send()
        cr.send = gen.send
        return cr

    def _run(self, *args, **kwargs):
        raise NotImplementedError("no target specified for coroutine %r" %
                                  self)
    run = _run
    
    def _send(self, arg):
        raise TypeError("Coroutine sent value before start", self)
    send = _send

    def clone(self):
        return Coroutine(target=self.run, name=self.__name__, doc=self.__doc__)

    @property
    def running(self):
        return self.__running

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

def always(fsa):
    '''Always true'''
    return True

class Case(State):
    '''An fsa.State that includes a test case function.'''
    def __init__(self, state=state, when=always, reason='', args=(), kwargs={}):
        self.when = when
        self.reason = reason
        self.__args = args
        self.__kwargs = kwargs
        super(Case, self).__init__(target=state.run, name=state.__name__,
                doc=state.__doc__, _dowrap=False, **state.states)

    def prepare(self, *args, **kwargs):
        c = self.clone()
        c.__args = c.__args + args
        c.__kwargs.update(kwargs)
        return c
    
    def check(self, fsa):
        return self.when(fsa, *self.__args, **self.__kwargs)

    def clone(self):
        return Case(state=self, when=self.when, reason=self.reason,
                    args=self.__args, kwargs=self.__kwargs)


##
# FSA implementation
##

# action bitmasks
FSA_INPUT = 0
FSA_YIELD = 1
FSA_PUSH = 2
FSA_POP = 4
FSA_SWAP = 6

# repeated action bitmasks
FSA_REPEAT = 8
FSA_SKIP = 9
FSA_PUSHALL = 10
FSA_POPMANY = 12

class FSA(State):
    '''Finite State Automaton implementation using coroutines.
    
    Implements a core run() method, plus several helper functions that
    mimic the previous FSA API.  Each call to step() sends the a reference
    to the FSA into its currently running State.  If an input function is
    provided it will be called with no arguments each frame and will be
    accessible through the FSA.input variable.
    '''
    def __init__(self, target, input=None, **kwargs):
        super(FSA, self).__init__(**kwargs)
        self.__initial = target
        if input is not None and not hasattr(input, '__call__'):
            raise TypeError('input argument must be callable')
        self.__input = input
        self.input = None

    def step(self):
        if self.__input:
            self.input = self.__input()
        try:
            self.send((FSA_INPUT, self))
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

            FSA_REPEAT
                Generally, indicates that an operation should be performed
                multiple times.

            FSA_SKIP
                Equivalent to FSA_YIELD | FSA_REPEAT.  The value is a
                number of frames to skip (i.e. yield).  Note that the count
                includes the current frame
                (e.g. 5 yields total = this frame + 4 others)

            FSA_PUSHALL
            FSA_POPMANY
                These are not yet implemented, but you can guess what they
                should do.  There remains some complexities about how to
                handle combinations of these calls with FSA_SKIP.  Perhaps
                this should be disallowed.
        '''
        action = input = value = None
        # initialize state stack
        stack = []
        if self.__initial:
            stack.append(self.__initial)
        # wait for initial action tuple
        action, input = yield
        start_time = time.time()
        while True:
            if debug:
                print "DEBUG: %s - (%i, %s)" % (self.__name__, action, value)
            # process action
            if action & FSA_POP:
                action ^= FSA_POP
                if action & FSA_REPEAT:
                    raise NotImplementedError("FSA_POPMANY not implemented")
                if not stack:
                    break
                stack.pop()
            if action & FSA_PUSH:
                action ^= FSA_PUSH
                if action & FSA_REPEAT:
                    raise NotImplementedError("FSA_PUSHALL not implemented")
                stack.append(value)
            if action & FSA_YIELD:
                # wait for next input
                if verbose:
                    print ('%r: frame completed in %f' %
                            (self, time.time() - start_time))
                if action & FSA_REPEAT:
                    action = FSA_INPUT
                    while action == FSA_INPUT and value:
                        action, input = yield value
                        value -= 1
                else:
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
        return self.__class__(target=self.__initial, input=self.__input,
                              name=self.__name__, doc=self.__doc__)

    def statedict(self):
        return {'initial': self.__initial}

    # simulate former FSA API
    @staticmethod
    def stay(value=None):
        ''' --> (FSA_YIELD, value).  Yield this result to stay in
        the current state but wait for the next vision frame.
        '''
        return FSA_YIELD, value

    @staticmethod
    def goNow(state):
        ''' --> (FSA_SWAP, state).  Yield this result to switch to a new
        state immediately.  When finished, return control to the parent
        state (exit this state).'''
        return (FSA_SWAP, state)

    def goNow_or_None(self, case):
        return case.check(self) and self.goNow(case) or None

    def goNow_or_yield(self, case):
        return case.check(self) and self.goNow(case) or self.stay()

    @staticmethod
    def goLater(state):
        ''' --> (FSA_SWAP | FSA_YIELD, state).  Yield this result to
        switch to a new state after waiting a single frame.  When
        finished, return control to the parent state (exit this state).'''
        return (FSA_SWAP | FSA_YIELD, state)

    @staticmethod
    def enterNow(state):
        ''' --> (FSA_PUSH, state).  Yield this result to enter a new
        state immediately.  When finished, return control to the current
        state (return where left off).'''
        return (FSA_PUSH, state)

    def enterNow_or_None(self, case):
        return case.check(self) and self.enterNow(case) or None

    def enterNow_or_yield(self, case):
        return case.check(self) and self.enterNow(case) or self.stay()

    @staticmethod
    def enterLater(state):
        ''' --> (FSA_PUSH | FSA_YIELD).  Yield this result to enter a
        new state after waiting a single frame.  When finished, return
        control to the current state (return where left off).'''
        return (FSA_PUSH | FSA_YIELD, state)

    @staticmethod
    def wait(nframe):
        ''' --> (FSA_SKIP, nframe).  Yield this result to skip ahead
        nframe frames.'''
        return (FSA_SKIP, nframe)

    def waitFor(self, case):
        @state
        def waitForCase(self):
            fsa = yield
            while not case.check(fsa):
                yield fsa.stay()
            yield (FSA_POP, None)
        return self.enterNow(waitForCase())

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
        fsa = yield
        print 'Hello %s%s' % (fsa.input, suffix)

    def always(fsa):
        '''Always true'''
        return True
    
    @state(
        name='Cheerful Greeter',
        doc='Greet every input with a cheerful hello!',
        hello=hello.case(when=always, reason='always'),
    )
    def greeter(self):
        fsa = yield
        while True:
            # Check our private 'hello' case of the 'hello' state
            if self.hello.check(fsa.input):
                # say hello to our friend
                yield self.hello.enter('!')
                # when hello() raises StopIteration, the FSA will yield
                # when next called, the FSA will re-enter here
            else:
                raise NotImplementedError("shouldn't reach here")

    def input_in(fsa, seq):
        return fsa.input in seq

    # An alternative implementation
    @state(
        is_friend=hello.case(when=input_in, reason='is a friend')
                         .partial('!'),
        default=hello.case(when=always, reason='otherwise')
    )
    def friend_greeter(self, friends):
        '''Greet my friends warmly.'''
        is_friend = self.is_friend.prepare(friends)
        fsa = yield
        while True:
            yield (fsa.enterNow_or_None(is_friend()) or
                    fsa.enterNow_or_yield(self.default()))

    @state(
        is_friend=hello.case(when=input_in, reason='is_a_friend')
    )
    def friends_only(self, friends):
        '''Greet only my friends.'''
        is_friend = self.is_friend.prepare(friends)
        fsa = yield
        while True:
            yield fsa.waitFor(is_friend)
            yield fsa.enterNow(is_friend())

    # Create a new FSA
    RawNameInputFSA = FSA(
        #target=greeter()
        #target=friend_greeter(['Billy', 'Joanna']),
        target=friends_only(['Joe', 'Susan']),
        input=functools.partial(raw_input, 'Enter your name: '),
        name='RawNameInputFSA',
        doc='read from stdin'
        )
    # Run the FSA
    args = sys.argv[1:]
    fsa = RawNameInputFSA(verbose='-v' in args, debug='-d' in args)
    print_tree(fsa)
    try:
        while True:
            fsa.step()
    except (KeyboardInterrupt, EOFError):
        print '\nGoodbye!'

