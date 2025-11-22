"""
Тесты для отчета.
"""

import pytest
from pathlib import Path
from reports.performance import PerformanceReport


def get_test_data_path(filename):
    return Path(__file__).parent / 'test_data' / filename


class TestPerformanceReport:
    
    def test_report_single_file(self):
        sample1_path = get_test_data_path('sample1.csv')
        if not sample1_path.exists():
            pytest.skip("sample1.csv не найден")
        
        report = PerformanceReport([sample1_path])
        report.generate()
        results = report.results
        
        assert len(results) == 5  # DevOps, Backend, Frontend, DevOps, QA
        performances = [r['average_performance'] for r in results]
        assert performances == sorted(performances, reverse=True)
    
    def test_report_multiple_files(self):
        sample1_path = get_test_data_path('sample1.csv')
        sample2_path = get_test_data_path('sample2.csv')
        
        if not sample1_path.exists() or not sample2_path.exists():
            pytest.skip("Тестовые файлы не найдены")
        
        report = PerformanceReport([sample1_path, sample2_path])
        report.generate()
        results = report.results
        
        assert len(results) == 5
        frontend_result = next(r for r in results if r['position'] == 'Frontend Developer')
        assert frontend_result['average_performance'] == pytest.approx(4.75, 0.01)  # (4.7 + 4.8) / 2
    
    def test_empty_file(self):
        empty_path = get_test_data_path('empty.csv')
        if not empty_path.exists():
            pytest.skip("empty.csv не найден")
        
        report = PerformanceReport([empty_path])
        with pytest.raises(Exception, match="Не удалось загрузить данные из файлов"):
            report.generate()
    
    def test_invalid_data_file(self):
        invalid_path = get_test_data_path('invalid_data.csv')
        if not invalid_path.exists():
            pytest.skip("invalid_data.csv не найден")
        
        report = PerformanceReport([invalid_path])
        report.generate()
        results = report.results
        
        assert len(results) == 1
        assert results[0]['position'] == 'Developer'
        assert results[0]['average_performance'] == 4.5
    
    def test_get_headers(self):
        report = PerformanceReport([])
        headers = report.get_headers()
        assert headers == ['position', 'average_performance']
    
    def test_display_method(self, capsys):
        sample1_path = get_test_data_path('sample1.csv')
        if not sample1_path.exists():
            pytest.skip("sample1.csv не найден")
        
        report = PerformanceReport([sample1_path])
        report.generate()
        report.display()
        
        captured = capsys.readouterr()
        assert len(captured.out) > 0
        assert 'position' in captured.out.lower()
        assert 'performance' in captured.out.lower()
    
    def test_specific_calculations(self):
        sample1_path = get_test_data_path('sample1.csv')
        if not sample1_path.exists():
            pytest.skip("sample1.csv не найден")
        
        report = PerformanceReport([sample1_path])
        report.generate()
        results = report.results
        
        backend_result = next(r for r in results if r['position'] == 'Backend Developer')
        assert backend_result['average_performance'] == 4.8
        
        frontend_result = next(r for r in results if r['position'] == 'Frontend Developer')
        assert frontend_result['average_performance'] == 4.7