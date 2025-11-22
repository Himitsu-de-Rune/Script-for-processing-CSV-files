"""
Отчет по эффективности сотрудников по позициям.
"""

from typing import List
from collections import defaultdict
from reports.base import BaseReport


class PerformanceReport(BaseReport):
    
    def process_data(self):
        position_data = defaultdict(list)
        
        for row in self.data:
            position = row['position']
            try:
                performance = float(row['performance'])
                position_data[position].append(performance)
            except (ValueError, KeyError):
                continue
        
        self.results = []
        for position, performances in position_data.items():
            if performances:
                avg_performance = sum(performances) / len(performances)
                self.results.append({
                    'position': position,
                    'average_performance': round(avg_performance, 2)
                })
        
        self.results.sort(key=lambda x: x['average_performance'], reverse=True)
    
    def get_headers(self) -> List[str]:
        return ['position', 'average_performance']