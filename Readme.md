# Транслятор для языка с оператором while

## Описание
Димитриев Егор КМБО-02-23

Архитектура программы:

сканер (лексер) - разбивает текст на токены, отделен от остального
парсер - рекурсивный нисходящий, строит AST
интерпретатор - вычисляет значение выражения

## Используемая грамматика

<Program> ::= <Statement>
<Statement> ::= <While> | <Print> | <Expression> ";"
<While> ::= "while" "(" <Condition> ")" <Statement>
<Condition> ::= <Expression> <ComparisonOp> <Expression>
<Expression> ::= <Primary> | "++" identifier | "--" identifier
<Primary> ::= identifier | number
<ComparisonOp> ::= "<" | ">" | "<=" | ">=" | "==" | "!="
<Print> ::= "print" "(" <Expression> ")" ";"


## Требования
- Python 3.6 или выше

## Установка

### 1. Клонируйте репозиторий

Склонируйте репозиторий с игрой с помощью следующей команды:

```bash
git clone https://github.com/Demos-gloryofRome44/TranslatorMirea.git
```

### Способы запуска программы

#### Способ 1: Чтение из файла (рекомендуется)


```bash
python3 main.py test.txt
```

```bash
# Создайте тестовые файлы
echo "while (++counter < 5) print(++result);" > example1.txt
echo "x = 10; while (x > 0) print(--x);" > example2.txt

# Запуск с разными файлами
python3 main.py example1.txt
python3 main.py example2.txt
```

#### Способ 2: Прямой ввод через pipe (перенаправление ввода)

```bash
echo "while (++a < 3) print(++b);" | python3 main.py
```

#### Способ 3: Интерактивный режим

Запустите программу без аргументов и вводите вручную:

```bash
python3 main.py
```
После запуска вы увидите приглашение:

```text
Введите исходный код (Ctrl+D для завершения ввода):
```
Введите код, например:

```text
while (++x < 3) print(++y);
```
Нажмите Ctrl+D (или Ctrl+Z на Windows) для завершения ввода и запуска анализа.