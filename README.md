# DeadlockReporter dumps the stack on deadlock

[![PyPI version](https://badge.fury.io/py/deadlockreporter.svg)](http://badge.fury.io/py/deadlockreporter)

## Usage

    $ sudo pip3 install deadlockreporter
    $ deadlockreporter -t 30 sh -c 'cd example; java Deadlock'
    [DeadlockReporter] Starting `sh -c cd example; java Deadlock`, timeout=5 seconds
    Alphonse: Gaston  has bowed to me!
    Gaston: Alphonse  has bowed to me!
    [DeadlockReporter] Timedout (5 seconds)
    [DeadlockReporter] Stack dump for java[pid=1265, exe=/usr/lib/jvm/java-7-openjdk-amd64/jre/bin/java, cmdline=java Deadlock] available:
    2015-10-22 14:57:21
    Full thread dump OpenJDK 64-Bit Server VM (24.79-b02 mixed mode):
    
    "Attach Listener" daemon prio=10 tid=0x00007f6204001000 nid=0x542 waiting on condition [0x0000000000000000]
       java.lang.Thread.State: RUNNABLE
    
    "DestroyJavaVM" prio=10 tid=0x00007f623000a000 nid=0x4f2 waiting on condition [0x0000000000000000]
       java.lang.Thread.State: RUNNABLE
    
    "Thread-1" prio=10 tid=0x00007f62300ff000 nid=0x500 waiting for monitor entry [0x00007f6216d3a000]
       java.lang.Thread.State: BLOCKED (on object monitor)
            at Deadlock$Friend.bowBack(Deadlock.java:19)
            - waiting to lock <0x00000007acccf640> (a Deadlock$Friend)
	..		

## Supported language runtimes
* Any language that runs on JVM

### How to support other languages
Follow this example for Java:
```python
def java_matcher(p):
	assert isinstance(p, psutil.Process)
	return p.name() == 'java'

def java_dumper(p):
	assert isinstance(p, psutil.Process)
	jstack = psutil.Popen(['jstack', str(p.pid)],
						  stdout=sys.stdout,
						  stderr=sys.stderr)
	jstack.wait()

assert isinstance(command, list) # e.g. ["java", "-jar", "foobar.jar"]
assert isinstance(timeout, int) # in seconds
dlr = DeadlockReporter(command, timeout)
dlr.register_stack_dumper(java_matcher, java_dumper)
dlr.run()
```
