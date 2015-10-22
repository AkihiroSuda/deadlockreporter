import argparse
import sys
from deadlockreporter.core import DeadlockReporter


def main():
    parser = argparse.ArgumentParser(
        description='DeadlockReporter dumps the stack on deadlock')
    parser.add_argument('COMMAND',
                        type=str,
                        nargs=argparse.REMAINDER,
                        help="command")
    parser.add_argument('-t', '--timeout',
                        required=True,
                        type=int,
                        help='timeout seconds')
    parser.add_argument('--kill-on-timeout',
                        action='store_true',
                        help='kill on timeout')

    args = parser.parse_args()
    dlr = DeadlockReporter(args.COMMAND,
                           args.timeout,
                           args.kill_on_timeout)
    dlr.register_known_stack_dumpers()
    dlr.run()


if __name__ == '__main__':
    sys.exit(main())
