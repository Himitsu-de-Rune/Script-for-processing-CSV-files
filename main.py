"""
Основной скрипт.
"""

import argparse
import sys
from pathlib import Path
from reports.performance import PerformanceReport


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Генерация отчетов из CSV файлов с данными сотрудников'
    )
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='Пути к CSV файлам с данными'
    )
    parser.add_argument(
        '--report',
        choices=['performance'],
        required=True,
        help='Тип отчета для генерации'
    )
    return parser.parse_args()


def validate_files(file_paths):
    valid_files = []
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            print(f'Предупреждение: файл {file_path} не существует', file=sys.stderr)
            continue
        if not path.is_file():
            print(f'Предупреждение: {file_path} не является файлом', file=sys.stderr)
            continue
        valid_files.append(path)
    
    if not valid_files:
        print('Ошибка: не найдено ни одного валидного файла', file=sys.stderr)
        sys.exit(1)
    
    return valid_files


def get_report_class(report_type):
    report_classes = {
        'performance': PerformanceReport,
    }
    return report_classes.get(report_type)


def main():
    args = parse_arguments()
    
    valid_files = validate_files(args.files)
    
    report_class = get_report_class(args.report)
    if not report_class:
        print(f'Ошибка: неизвестный тип отчета {args.report}', file=sys.stderr)
        sys.exit(1)
    
    try:
        report = report_class(valid_files)
        report.generate()
        report.display()
    except Exception as e:
        print(f'Ошибка при генерации отчета: {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()