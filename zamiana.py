from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import argparse
import json
import yaml
import xml.etree.ElementTree as ET

def parse_arguments():
	parser = argparse.ArgumentParser(description="Konwersja danych między formatami .xml, .json i .yml.")
	parser.add_argument('input_file', type=str)
	parser.add_argument('output_file', type=str)
	args = parser.parse_args()
	return args.input_file, args.output_file

#if __name__ == "__main__":
#	input_file, output_file = parse_arguments()
	

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

def save_yaml(data, file_path):
	try:
		with open(file_path, 'w', encoding='utf-8') as file:
			yaml.safe_dump(data, file, default_flow_style=False, allow_unicode=True)
		print("Dane zostały zapisane do pliku YAML.")
	except Exception as e:
		print(f"Nieoczekiwany błąd podczas zapisu do pliku YAML: {e}")

def load_xml(file_path):
	try:
		tree=ET.parse(file_path)
		root=tree.getroot()
		print("Plik XML został poprawnie wczytany.")
		return root
	except ET.ParseError as e:
		print(f"Błąd składni XML: {e}")
	except FileNotFoundError:
		print(f"Plik {file_path} nie został znaleziony.")
	except Exception as e:
		print(f"Nieoczekiwany błąd: {e}")
		return None

def save_xml(data, file_path):
	try:
		tree=ET.ElementTree(data)
		tree.write(file_path, encoding='utf-8', xml_declaration=True)
		print("Dane zostały zapisane do pliku XML.")
	except Exception as e:
		print(f"Nieoczekiwany błąd podaczas zapisu do pliku XML: {e}")

class FileLoader(QThread):
	finished = pyqtSignal(object)

	def __init__(self, file_path, file_type):
		super().__init__()
		self.file_path = file_path
		self.file_type = file_type

	def run(self):
		if self.file_type == 'json':
			data = load_json(self.file_path)
		elif self.file_type == 'yaml':
			data = load_yaml(self.file_path)
		elif self.file_type == 'xml':
			data = load_xml(self.file_path)
		else:
			data = None
		self.finished.emit(data)

class FileSaver(QThread):
	def __init__(self, data, file_path, file_type):
		super().__init__()
		self.data = data
		self.file_path = file_path
		self.file_type = file_type

	def run(self): 
		if self.file_type == 'json':
			save_json(self.data, self.file_path)
		elif self.file_type == 'yaml':
			save_yaml(self.data, self.file_path)
		elif self.file_type == 'xml':
			save_xml(self.data, self.file_path)

class ConverterApp(QMainWindow):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setGeometry(100, 100, 400, 200)
		self.setWindowTitle('Konwerter danych')

		self.label = QLabel('Wybierz plik wejściowy:', self)
		self.label.move(20, 20)

		self.input_button = QPushButton('Wybierz plik', self)
		self.input_button.move(20, 50)
		self.input_button.clicked.connect(self.open_input_file)

		self.output_button = QPushButton('Wybierz ścieżkę', self)
		self.output_button.move(20, 100)
		self.output_button.clicked.connect(self.open_output_file)

		self.convert_button = QPushButton('Konwertuj', self)
		self.convert_button.move(20, 150)
		self.convert_button.clicked.connect(self.convert_file)

		self.input_file_path = ''
		self.output_file_path = ''
		self.data = None

	def open_input_file(self):
		options = QFileDialog.Options()
		file, _ = QFileDialog.getOpenFileName(self, 'Wybierz plik wejściowy', '', 'Wszystkie pliki (*);;Pliki JSON (*.json);;Pliki YAML (*.yaml *.yml);;Pliki XML (*.xml)', options=options)
		if file:
			self.input_file_path = file
			self.load_file()

	def open_output_file(self):
		options = QFileDialog.Options()
		file, _ = QFileDialog.getSaveFileName(self, 'Wybierz ścieżkę zapisu', '', 'Pliki JSON (*.json);;Pliki YAML (*.yaml *.yml);;Pliki XML (*.xml)', options=options)
		if file:
			self.output_file_path = file

	def load_file(self):
		file_type = self.input_file_path.split('.')[-1]
		self.loader_thread = FileLoader(self.input_file_path, file_type)
		self.loader_thread.finished.connect(self.on_load_finished)
		self.loader_thread.start()

	def on_load_finished(self, data):
		self.data = data

	def convert_file(self):
		if self.input_file_path and self.output_file_path and self.data is not None:
			output_type = self.output_file_path.split('.')[-1]
			self.saver_thread = FileSaver(self.data, self.output_file_path, output_type)
			self.saver_thread.start()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = ConverterApp()
	ex.show()
	sys.exit(app.exec_())
