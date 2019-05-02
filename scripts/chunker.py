import argparse
import json
import sys


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--chunksize",
        dest="chunksize",
        type=int,
        default=65536,
        help="size of chunks",
    )
    parser.add_argument(
        "-f",
        "--filename",
        dest="filename",
        default=None,
        help="name of file to read",
    )
    parser.add_argument(
        "-u",
        "--uri",
        dest="uri",
        default=None,
        help="name of file to read",
        required=True
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if args.filename:
        input_file = open(args.filename)
    else:
        input_file = sys.stdin
    
    while True:
        chunk = input_file.read(args.chunksize)
        if not chunk:
            return
        chunk = {"uri": args.uri,
                 "chunk": chunk}
        print json.dumps(chunk)

if __name__ == "__main__":
    main()
    