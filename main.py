import sys
import os

from scanner import Scanner, TokenType, Token
from parser import Parser, ParseError
from semantic import SemanticAnalyzer, SemanticError

def main():
    # Чтение исходного кода
    if len(sys.argv) > 1:
        # Из файла
        filename = sys.argv[1]
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                source = f.read()
            print(f"Чтение из файла: {filename}")
        else:
            print(f"Файл не найден: {filename}")
            return
    else:
        # Из стандартного ввода (pipe или интерактивный режим)
        if not sys.stdin.isatty():
            source = sys.stdin.read()
        else:
            print("Введите исходный код (Ctrl+D для завершения ввода):")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            source = '\n'.join(lines)
    
    if not source.strip():
        print("Входные данные пусты")
        return
    
    print("\n" + "="*50)
    print("ИСХОДНЫЙ КОД:")
    print("="*50)
    print(source)
    print("="*50)
    
    try:
        # 1. Лексический анализ
        print("\n" + "="*50)
        print("ЛЕКСИЧЕСКИЙ АНАЛИЗ:")
        print("="*50)
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        
        for token in tokens:
            print(token)
        
        # 2. Синтаксический анализ
        print("\n" + "="*50)
        print("СИНТАКСИЧЕСКИЙ АНАЛИЗ:")
        print("="*50)
        parser = Parser(tokens)
        ast = parser.parse()
        
        if ast:
            print("AST построен успешно")
            print("AST структура:", ast)
            
            # 3. Семантический анализ и выполнение
            print("\n" + "="*50)
            print("ВЫПОЛНЕНИЕ:")
            print("="*50)
            analyzer = SemanticAnalyzer()
            analyzer.execute(ast)
            
            print("\n" + "="*50)
            print("СОСТОЯНИЕ ПЕРЕМЕННЫХ:")
            print("="*50)
            for var, value in analyzer.variables.items():
                print(f"{var} = {value}")
        else:
            print("Ошибка: AST не построен")
        
    except SyntaxError as e:
        print(f"\nОШИБКА СКАНИРОВАНИЯ: {e}")
    except ParseError as e:
        print(f"\nОШИБКА ПАРСИНГА: {e}")
    except SemanticError as e:
        print(f"\nСЕМАНТИЧЕСКАЯ ОШИБКА: {e}")
    except Exception as e:
        print(f"\nНЕИЗВЕСТНАЯ ОШИБКА: {e}")

if __name__ == "__main__":
    main()