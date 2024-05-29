import sys
import argparse
import json
import yaml

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

def save_json(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Dane zostały zapisane do pliku JSON.")
    except Exception as e:
        print(f"Nieoczekiwany błąd podczas zapisu do pliku JSON: {e}")

def load_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        print("Plik YAML został poprawnie wczytany.")
        return data
    except yaml.YAMLError as e:
        print(f"Błąd składni YAML: {e}")
    except FileNotFoundError:
        print(f"Plik {file_path} nie został znaleziony.")
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")
        return None
