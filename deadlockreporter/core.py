from __future__ import print_function
import logging
import psutil
import sys


def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(
        '[DeadlockReporter] %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


LOG = init_logger()


class ProcessUtil:
    @classmethod
    def stringify(cls, p, verbose=False):
        assert isinstance(p, psutil.Process)
        cmdline = ' '.join(p.cmdline())
        lim = 32
        if len(cmdline) > lim and not verbose:
            cmdline = cmdline[0:lim] + '..'
        return '%s[pid=%d, exe=%s, cmdline=%s]' % (p.name(), p.pid, p.exe(), cmdline)

    @classmethod
    def dump_tree(cls, p, fn=lambda x: print(x)):
        assert isinstance(p, psutil.Process)
        fn('Process %s' % cls.stringify(p))
        for c in p.children(recursive=True):
            fn('Descendant Process %s' % cls.stringify(c))

    @classmethod
    def kill_tree(cls, p):
        assert isinstance(p, psutil.Process)
        assert isinstance(p, psutil.Process)
        LOG.info('Killing %s', cls.stringify(p))
        for c in p.children(recursive=True):
            LOG.info('Killing %s', cls.stringify(c))
            c.kill()
        p.kill()


class DeadlockReporter(object):
    def __init__(self, command, timeout, kill_on_timeout=False):
        assert isinstance(command, list)
        assert isinstance(timeout, int)
        assert isinstance(kill_on_timeout, bool)
        self.command = command
        self.timeout = timeout
        self.kill_on_timeout = kill_on_timeout
        self._stack_dumpers = {}

    def register_stack_dumper(self,
                              matcher=lambda p: False,
                              dumper=lambda p: print(p)):
        self._stack_dumpers[matcher] = dumper

    def _try_stack_dumpers(self, p):
        for matcher, dumper in self._stack_dumpers.items():
            matched = matcher(p)
            if matched:
                LOG.info('Stack dump for %s available:',
                         ProcessUtil.stringify(p))
                dumper(p)

    def _on_timeout(self, p, e):
        assert isinstance(p, psutil.Process)
        assert isinstance(e, psutil.TimeoutExpired)

        LOG.info('Timed out (%d seconds)', e.seconds)

        self._try_stack_dumpers(p)
        for c in p.children(recursive=True):
            self._try_stack_dumpers(c)

        if self.kill_on_timeout:
            LOG.info('Killing the process')
            ProcessUtil.kill_tree(p)
            sys.exit(1)
        else:
            p.wait()

    def run(self):
        LOG.info('Starting `%s`, timeout=%d seconds',
                 ' '.join(self.command), self.timeout)
        p = psutil.Popen(self.command,
                         stdin=sys.stdin,
                         stdout=sys.stdout,
                         stderr=sys.stderr)
        try:
            p.wait(self.timeout)
        except psutil.TimeoutExpired as te:
            self._on_timeout(p, te)

    def register_known_stack_dumpers(self):

        def java_matcher(p):
            assert isinstance(p, psutil.Process)
            return p.name() == 'java'

        def java_dumper(p):
            assert isinstance(p, psutil.Process)
            jstack = psutil.Popen(['jstack', str(p.pid)],
                                  stdout=sys.stdout,
                                  stderr=sys.stderr)
            jstack.wait()

        self.register_stack_dumper(java_matcher, java_dumper)
