#! /bin/env python3
"""
Helper python script for the swanctl autocompletion bash script.
Provides the ability to list 
"""
import argparse
import itertools
import shlex
import sys

#import vici

def eprint(*args, **kwargs):
    """
    Print to stderr
    """
    stream = open("completion_test", "a")
    print(*args, file=stream, **kwargs)


class SwanctlAutoComplete():
    """
    Implements the code for swanctl autocompletion
    """
    long_commands = ["--counters", "--initiate", "--terminate", "--rekey",
                     "--redirect", "--uninstall", "--install", "--list-sas",
                     "--monitor-sa", "--list-pols", "--list-authorities",
                     "--list-conns", "--list-certs", "--list-pools",
                     "--list-algs", "--flush-certs", "--load-all",
                     "--load-authorities", "--load-conns", "--load-creds",
                     "--load-pools", "--log", "--version", "--stats",
                     "--reload-settings", "--help"]
    short_commands = ["-C", "-i", "-t", "-R", "-d", "-u", "-p", "-l", "-m",
                      "-P", "-B", "-L", "-x", "-A", "-g", "-f", "-q", "-b",
                      "-c", "-s", "-a", "-T", "-v", "-s", "-r", "-h"]
    options = ["--help", "-h", "--raw", "-r", "--pretty", "-P", "--debug",
               "-v", "--options", "-+", "--uri", "-u"]
    
    @classmethod
    def main(cls):
        argparser = argparse.ArgumentParser()
        argparser.add_argument("-c")
        argparser.add_argument(
            "-+", "--uri",
            help="URI to strongswan vici service",
            type=str,
            nargs="+")
        argparser.add_argument(
            "--cword")
        argparser.add_argument(
            "--cur")
        argparser.add_argument(
            "--prev")
        argparser.add_argument(
            "--words")

        known_args, unknown_args = argparser.parse_known_args()
        cls.switch_on_command(known_args)

    @classmethod
    def filter_opts(cls, orig_opts, possible_opts):
        # special handling for conflicting options
        # raw and pretty
        conflicting = ["--raw", "-r", "--pretty", "-P"]
        filtered_opts = {}
        for opt_short, opt_long in possible_opts:
            filtered_opts[opt_short] = 0
            filtered_opts[opt_long] = 0
        for word in ["--raw", "-r", "--pretty", "-P"]:
            if word in filtered_opts:
                for word2 in conflicting:
                    try:
                        filtered_opts.pop(word2)
                    except:
                        pass
        for word in orig_opts:
            for opt_short, opt_long in possible_opts:
                if word in (opt_short, opt_long):
                    try:
                        filtered_opts.pop(opt_short)
                    except:
                        pass
                    try:
                        filtered_opts.pop(opt_long)
                    except:
                        pass
        return filtered_opts

    @classmethod
    def filter_opts_conflicting(cls, orig_opts, possible_opts, conflicting_opts_groups):
        filtered_opts = {}
        for opt_short, opt_long in possible_opts:
            filtered_opts[opt_short] = 0
            filtered_opts[opt_long] = 0
        # iterate over tuples of ((short_opt, long_opt), (short_opt, long_opt))
        for conflicting_opts_group in conflicting_opts_groups:
            for conflicting_opt_short_long in conflicting_opts_group:
                for word in conflicting_opt_short_long:
                    if word in orig_opts:
                        for opt in itertools.chain(*conflicting_opts_group):
                            try:
                                filtered_opts.pop(opt)
                            except:
                                pass
        for word in orig_opts:
            for opt_short, opt_long in possible_opts:
                if word in (opt_short, opt_long):
                    try:
                        filtered_opts.pop(opt_short)
                    except:
                        pass
                    try:
                        filtered_opts.pop(opt_long)
                    except:
                        pass
        return filtered_opts

    @classmethod
    def check_opts(cls, group1, group2):
        for item1 in group1:
            for item2 in group2:
                if item1 == item2:
                    return True
        return False

    @classmethod
    def switch_on_command(cls, args):
        """
        Handle the different commands
        """
        # available environment variables regarding completion
        # are cur prev words and cword
        # cur: Current word that autocompletion is attempted on
        # prev: previous word
        # words: bash array of all words
        # cword: count of words

        def ike_sa_name_handler(filtered_opts):
            print(" ")
            sys.exit(0)
        def child_sa_name_handler(filtered_opts):
            print(" ")
            sys.exit(0)
        def ike_id_handler(filtered_opts):
            print(" ")
            sys.exit(0)
        def child_id_handler(filtered_opts):
            print(" ")
            sys.exit(0)
        def pool_handler(filtered_opts):
            print(" ")
            sys.exit(0)
        def timeout_handler(filtered_opts):
            print(" ")
            sys.exit(0)
        def file_handler(filtered_opts):
            # returnstatus 4 is handled by the shell script as prompt to
            # run _filedir
            print(" ")
            sys.exit(4)
        def url_handler(filtered_opts):
            print(" ")
            # returnstatus 5 is handled by the shell script as prompt to
            # run _known_hosts_real or other handler to get known hosts
            sys.exit(5)
        words = shlex.split(str(args.words))

        cur = args.cur
        prev = args.prev

        cword = int(args.cword, 10)
        general_opts = [("-h", "--help"), ("-r", "--raw"), ("-P", "--pretty"),
                        ("-v", "--debug"), ("-+", "--options"), ("-u", "--uri")]

        # cword can not be 0 if called correctly, so no reason to check it
        if cword == 1:
            # only binary name "swanctl" given, print out all possible commands
            print(str.join(" ", cls.long_commands + cls.short_commands))
            sys.exit(0)

        command = words[1]
        # deal with general opts
        general_opts = cls.filter_opts(words, general_opts)
        # no suggestions if help message is asked
        if cls.check_opts((prev, cur), ("-h", "--help")):
            sys.exit(0)
        if cls.check_opts((prev, cur), ("-u", "--uri")):
            url_handler(general_opts)
        if cls.check_opts((prev, cur), ("--options", "-+")):
            file_handler(general_opts)
        if cls.check_opts((prev, cur), ("-v", "--debug")):
            print("-1 0 1 2 3 4")
            sys.exit(0)

        if command in ("--counters", "-C"):
            opts = [("-n", "--name"), ("-a", "--all"), ("-R", "--reset")]
            filtered_opts = cls.filter_opts_conflicting(
                words, opts, [(("-n", "--name"), ("-a", "--all"))])

            if cls.check_opts((prev, cur), ("-n", "--name")):
                ike_sa_name_handler(filtered_opts)
            print(" ".join(itertools.chain(filtered_opts.keys(),
                                           general_opts)))
        elif command in ("--initiate", "-i"):
            opts = [("-c", "--child"), ("-i", "--ike")]
            filtered_opts = cls.filter_opts(words, opts)
            if cls.check_opts((prev, cur), ("-c", "--child")):
                child_sa_name_handler(filtered_opts)
            if cls.check_opts((prev. cur), ("-i", "--ike")):
                ike_sa_name_handler(filtered_opts)
            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        elif command in ("-t", "--terminate"):
            opts = [("-c", "--child"), ("-i", "--ike"), ("-C", "--child-id"),
                    ("-I", "--ike-id"), ("-f", "--force"), ("-t", "--timeout")]
            filtered_opts = cls.filter_opts_conflicting(
                words, opts, [(("-C", "--child-id"), ("-I", "--ike-id"))])

            # deal with child_sa name
            if cls.check_opts((prev, opts), ("-c", "--child")):
                child_sa_name_handler(filtered_opts)
            # deal with ike_sa name
            if cls.check_opts((prev, opts), ("-i", "--ike")):
                ike_sa_name_handler(filtered_opts)
            # deal with child IDs
            if cls.check_opts((prev, opts), ("-C", "--child-id")):
                child_id_handler(filtered_opts)
            # deal with ike_sa IDs
            if cls.check_opts((prev, opts), ("-I", "--ike-id")):
                ike_id_handler(filtered_opts)
            if cls.check_opts((prev, opts), ("-t", "--timeout")):
                timeout_handler(filtered_opts)
            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        elif command in ("-R", "--rekey"):
            opts = [("-c", "--child"), ("-i", "--ike"), ("-C", "--child-id"),
                    ("-I", "--ike-id"), ("-a", "--reauth")]
            filtered_opts = cls.filter_opts_conflicting(
                words, opts, [(("-C", "--child-id"), ("-I", "--ike-id"))])

            # deal with child_sa name
            if cls.check_opts((prev, opts), ("-c", "--child")):
                sys.exit(0)
            # deal with ike_sa name
            if cls.check_opts((prev, opts), ("-i", "--ike")):
                ike_sa_name_handler(filtered_opts)
            # deal with child IDs
            if cls.check_opts((prev, opts), ("-C", "--child-id")):
                child_id_handler(filtered_opts)
            # deal with ike_sa IDs
            if cls.check_opts((prev, opts), ("-I", "--ike-id")):
                ike_id_handler(filtered_opts)

            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        elif command in ("-d", "--redirect"):
            opts = [("-i", "--ike"), ("-I", "--ike-id"), ("p", "--peer-id"),
                    ("-g", "--gateway")]
            filtered_opts = cls.filter_opts(words, opts)

            # deal with child_sa name
            if cls.check_opts((prev, opts), ("-c", "--child")):
                child_sa_name_handler(filtered_opts)
            # deal with ike_sa name
            if cls.check_opts((prev, opts), ("-i", "--ike")):
                ike_sa_name_handler(filtered_opts)
            # deal with child IDs
            if cls.check_opts((prev, opts), ("-C", "--child-id")):
                child_id_handler(filtered_opts)
            # deal with ike_sa IDs
            if cls.check_opts((prev, opts), ("-I", "--ike-id")):
                ike_id_handler(filtered_opts)

            if cls.check_opts((prev, opts), ("-p", "--peer-id", "-g", "--gateway")):
                sys.exit(0)

            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))

        elif command in ("-u", "--uninstall", "-p", "--install"):
            opts = [("-i", "--ike"), ("-c", "--child")]
            filtered_opts = cls.filter_opts(words, opts)

            if cls.check_opts((prev, opts), ("-i", "--ike")):
                ike_sa_name_handler(filtered_opts)
            if cls.check_opts((prev, opts), ("-c", "--child")):
                child_sa_name_handler(filtered_opts)

            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        elif command in ("-l", "--list-sas"):
            opts = [("-i", "--ike"), ("-I", "--ike-id")]
            filtered_opts = cls.filter_opts(words, opts)

            if cls.check_opts((prev, opts), ("-i", "--ike")):
                ike_sa_name_handler(filtered_opts)
            if cls.check_opts((prev, opts), ("-I", "--ike-id")):
                ike_id_handler(filtered_opts)

            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        elif command in ("-P", "--list-pols"):
            opts = [("-c", "--child"), ("-t", "--trap"), ("-d", "--drop"),
                    ("-p", "--pass")]
            filtered_opts = cls.filter_opts(words, opts)

            if cls.check_opts((prev, opts), ("-c", "--child")):
                child_sa_name_handler(filtered_opts)

            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        elif command in ("-B", "--list-authorities"):
            opts = [("-n", "--name")]
            filtered_opts = cls.filter_opts(words, opts)

            if cls.check_opts((prev, opts), ("-n", "--name")):
                sys.exit(0)
            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        elif command in ("-x", "--list-certs"):
            opts = [("-s", "--subject"), ("-t", "--type"), ("-f", "--flag"),
                    ("-p", "--pem"), ("-S", "--short"), ("-U", "--utc")]
            filtered_opts = cls.filter_opts(words, opts)

            if cls.check_opts((prev, opts), ("-s", "--subject")):
                sys.exit(0)
            if cls.check_opts((prev, opts), ("-t", "--type")):
                print("x509 x509_ac x509_crl ocsp_response pubkey")
                sys.exit(0)
            if cls.check_opts((prev, opts), ("-f", "--flag")):
                print("none ca aa ocsp any")
                sys.exit(0)
            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        elif command in ("-A", "--list-pools"):
            opts = [("-l", "--leases"), ("-n", "--name"), ("-f", "--file")]
            filtered_opts = cls.filter_opts(words, opts)

            if cls.check_opts((prev, opts), ("-n", "--name")):
                # handle pool name
                pool_handler(filtered_opts)
            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        elif command in ("-f", "--flush-certs"):
            opts = [("-t", "--type")]
            filtered_opts = cls.filter_opts(words, opts)

            if cls.check_opts((prev, opts), ("-t", "--type")):
                print("x509 x509_ac x509_crl ocsp_response pubkey")
                sys.exit(0)
            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        elif command in ("-q", "--load-all"):
            opts = [("-c", "--clear"), ("-n", "--noprompt"), ("-f", "--file")]
            filtered_opts = cls.filter_opts(words, opts)

            if cls.check_opts((prev, opts), ("-f", "--file")):
                file_handler(filtered_opts)
            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        elif command in ("-b", "--load-authorities"):
            opts = [("-f", "--file")]
            filtered_opts = cls.filter_opts(words, opts)

            if cls.check_opts((prev, opts), ("-f", "--file")):
                file_handler(filtered_opts)
            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        elif command in ("-c", "--load-conns"):
            opts = [("-f", "--file")]
            filtered_opts = cls.filter_opts(words, opts)

            if cls.check_opts((prev, opts), ("-f", "--file")):
                file_handler(filtered_opts)
            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        elif command in ("-s", "--load-creds"):
            opts = [("-c", "--clear"), ("-n", "--noprompt"), ("-f", "--file")]
            filtered_opts = cls.filter_opts(words, opts)

            if cls.check_opts((prev, opts), ("-f", "--file")):
                file_handler(filtered_opts)
            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        elif command in ("-a", "--load-pools"):
            opts = [("-c", "--clear"), ("-n", "--noprompt"), ("-f", "--file")]
            filtered_opts = cls.filter_opts(words, opts)

            if cls.check_opts((prev, opts), ("-f", "--file")):
                file_handler(filtered_opts)
            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        elif command in ("-v", "--version"):
            opts = [("-d", "--daemon")]
            filtered_opts = cls.filter_opts(words, opts)

            print(str.join(" ", itertools.chain(filtered_opts.keys(),
                                                general_opts)))
        else:
            # no matching command, exit
            print()
            sys.exit(0)

if __name__ == "__main__":
    SwanctlAutoComplete.main()