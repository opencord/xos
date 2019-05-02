import argparse
import json
import sys


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
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

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if args.filename:
        output_file = open(args.filename)
    else:
        output_file = sys.stdout
    
    data = sys.stdin.read()
    data = data.split("Response trailers received:\n")[0]
    parts = data.split("Response contents:\n")
    parts = parts[1:]
    for part in parts:
        part = part.strip("\n")
        if part:
            output_file.write(json.loads(part)["chunk"])


if __name__ == "__main__":
    main()
