#!/usr/bin/python

import argparse
from wprecon import WPRecon
from exploit_grabber import ExploitGrabber
import exploit_grabber
from inspect import isclass


def main(url, grabber, recon, proxy):
    """
    Main method, start scan, and exploit retrieving
    """
    wprecon = WPRecon(proxy)
    wprecon_results = wprecon.scan(url)

    print_recon(wprecon_results)
    if not recon:
        print_sploits(wprecon_results)


def print_recon(wprecon_results):
    # Recon
    for name, result in wprecon_results['printable_results'].items():
        if result is not None:
            print "[*] %s" % name
            if isinstance(result, list):
                for result_line in result:
                    print "  [+] %s" % result_line
            else:
                print "  [+] %s" % result


def print_sploits(wprecon_results):
    # Search sploits
    print "[*] Modules"
    grabbers = get_grabbers()
    for grabber in grabbers:
        grabber_obj = grabber()

        # Search for vulnerable modules
        for module in wprecon_results['modules']:
            print "  [+] %s" % module
            sploits = grabber_obj.search(module)
            for sploit in sploits:
                print "    [!] %s" % sploit

        # Search them related sploits
        theme = wprecon_results['printable_results']['Theme']
        if theme is not None:
            sploits = grabber_obj.search(theme)
            for sploit in sploits:
                print "  [+] %s" % sploit

        # Search wordpress version related sploits
        version = wprecon_results['printable_results']['Version']
        if version is not None:
            sploits = grabber_obj.search(version)
            for sploit in sploits:
                print "  [+] %s" % sploit


def get_grabbers():
    """
    Get all exploit grabber classes
    """
    grabbers = []
    for classname in dir(exploit_grabber):
        try:
            custom_class = getattr(exploit_grabber, classname)
            if isclass(custom_class):
                if issubclass(custom_class, ExploitGrabber):
                    if custom_class.__name__ != ExploitGrabber.__name__:
                        grabbers.append(custom_class)
        except TypeError:
            pass
    return grabbers


if __name__ == "__main__":
    """
    Entrypoint
    """
    print """
   -----------------------------------------
   | Imagine a fucking awesome title here  |
   | (like t-rex shooting lasers and stuff)|
   -----------------------------------------
    """
    parser = argparse.ArgumentParser(description='Sploit Wordpress for fun')
    parser.add_argument('-u', '--url',
                        action='store',
                        dest='url',
                        required=True,
                        help='victim url')
    parser.add_argument('-g', '--grabber',
                        action='store',
                        dest='grabber',
                        default='exploitdb',
                        help='Sploit grabber')
    parser.add_argument('-r', '--recon',
                        action='store_true',
                        dest='recon_only',
                        default=False,
                        help='Just recon')
    parser.add_argument('-t', '--tor',
                        action='store_true',
                        dest='tor',
                        default=False,
                        help='Use Tor')
    parser.add_argument('-p', '--proxy',
                        action='store',
                        dest='proxy',
                        default=None,
                        help='Use proxy')
    args = parser.parse_args()

    # Configure proxy
    proxy = None
    if args.tor:
        proxy = {"http": "127.0.0.1:9050",
                 "https": "127.0.0.1:9050"}

    if args.proxy is not None:
        proxy = {"http": args.proxy,
                 "https": args.proxy}

    main(args.url, args.grabber, args.recon_only, proxy)