import argparse


def main():
    parser = argparse.ArgumentParser(description="Develop and run your python application in clean Docker environments")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()
