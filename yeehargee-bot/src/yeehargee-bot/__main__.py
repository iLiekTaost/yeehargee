from argparse import ArgumentParser, Namespace
import os
import sys

def main():
    print('yeehargee!')
    print(f'os.environ["VERSION"] IS: {os.environ["VERSION"]}')

if __name__ == '__main__':
    sys.exit(main())