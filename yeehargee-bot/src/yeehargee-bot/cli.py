from argparse import ArgumentParser, Namespace

def parse_cli() -> Namespace:
    parser = ArgumentParser()
    # parser.add_subparsers('mode')
    parser.add_argument('token')
    return parser.parse_args()