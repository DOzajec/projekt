import sys
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Konwersja danych między formatami .xml, .json i .yml.")
    parser.add_argument('input_file', type=str)
    parser.add_argument('output_file', type=str)
    args = parser.parse_args()
    return args.input_file, args.output_file

if __name__ == "__main__":
    input_file, output_file = parse_arguments()
    print(f"Plik wejściowy: {input_file}")
    print(f"Plik wyjściowy: {output_file}")
