"""
Базовый класс для всех отчетов.
"""

from abc import ABC, abstractmethod
import csv
from pathlib import Path
from typing import List
from tabulate import tabulate


class BaseReport(ABC):
    
    def __init__(self, files: List[Path]):
        self.files = files
        self.data = []
        self.results = []
    
    def load_data(self):
        all_data = []
        for file_path in self.files:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    file_data = list(reader)
                    all_data.extend(file_data)
            except Exception as e:
                raise Exception(f'Ошибка чтения файла {file_path}: {e}')
        
        if not all_data:
            raise Exception('Не удалось загрузить данные из файлов')
        
        self.data = all_data
    
    @abstractmethod
    def process_data(self):
        pass
    
    @abstractmethod
    def get_headers(self) -> List[str]:
        pass
    
    def generate(self):
        self.load_data()
        self.process_data()
    
    def display(self):
        headers = self.get_headers()
        table_data = []
        
        for result in self.results:
            row = [result.get(header, '') for header in headers]
            table_data.append(row)
        
        print(tabulate(table_data, headers=headers, tablefmt='grid'))