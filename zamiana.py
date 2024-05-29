import sys
import argparse
import json

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

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        print("Plik JSON został poprawnie wczytany.")
        return data
    except json.JSONDecodeError as e:
        print(f"Błąd składni JSON: {e}")
    except FileNotFoundError:
        print(f"Plik {file_path} nie został znaleziony.")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")
        return None
