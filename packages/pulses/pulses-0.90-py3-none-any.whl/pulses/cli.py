"""
Usage:
    pulses [--gpio <gpio>] [--initial <initialMethod>] [--loop <loopMethod>]
                           [--final <finalMethod>] [--delay <delayMethod>]
                           [--min <min>] [--max <max>] [--delay-val <delay>]
                           [--verbose]

Options:
    -g --gpio=<gpio>         GPIO to use [default: 12]
    -i --initial=<method>    Initial method [default: linear]
    -l --loop=<method>       Loop method [default: sin]
    -f --final=<method>      Final method [default: linear]
    -d --delay=<method>      Delay method [default: constant]

    -m --min=<min>           Minimum value [default: 2]
    -M --max=<max>           Maximum value [default: 50]
    -D --delay-val=<delay>   Base delay value [default: 0.01]

    -V --verbose             Verbose mode [default: True]

    -h --help                Show help.
    -v --version             Show version.

""" # NOQA

import sys
import time
import logging
import signal
from docopt import docopt
from pulses import VERSION, ledPulse

logging.basicConfig(format="%(asctime)-15s %(levelname)5s %(name)s[%(process)d] %(threadName)s: %(message)s")


def signal_handler(sig, frame):
    print('stopping pulse...', end="", flush=True)
    led.stop()
    led.join()
    print('done.\nBailing out')
    sys.exit(0)


def main():
    global led

    args = docopt(__doc__, version=f'pulses {VERSION}')
    signal.signal(signal.SIGINT, signal_handler)

    log = logging.getLogger()
    log.setLevel('WARNING')
    if args.get('--verbose'):
        log.setLevel('DEBUG')
        log.info('setting verbose mode')

    led = ledPulse(int(args.get('--gpio')))

    params = {}
    for method in ['initial', 'loop', 'final']:
        methodName = args.get(f"--{method}")
        if methodName not in led.valueMethods:
            print(f"error: no value method '{methodName}' defined")
            sys.exit(1)
        params[f"{method}Method"] = methodName

    methodName = args.get("--delay")
    if methodName not in led.delayMethods:
        print(f"error: no delay method '{methodName}' defined")
        sys.exit(1)
    params['delayMethod'] = methodName

    params['min'] = int(args.get('--min'))
    params['max'] = int(args.get('--max'))
    params['delay'] = float(args.get('--delay-val'))

    print("-" * 20)
    print("pulses CLI test tool")
    print("-" * 20)
    print("\n> loop parameters")
    for param, value in params.items():
        print(f"  {param}: {value}")
    led.set(**params)
    print('\nstarting loop, press Ctrl-C to stop...')
    led.start()
    while True:
        time.sleep(4)


if __name__ == "__main__":
    main()
