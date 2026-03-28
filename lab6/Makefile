# GNU Bison + Flex (macOS: bison -d создаёт y.tab.c / y.tab.h)

CC = gcc
CFLAGS = -Wall -Wextra -std=c99

TARGET = analyzer
OBJS = main.o y.tab.o lex.yy.o

.PHONY: all clean test

all: $(TARGET)

y.tab.c y.tab.h: parser.y
	bison -d -o y.tab.c parser.y

lex.yy.c: lexer.l y.tab.h
	flex lexer.l

y.tab.o: y.tab.c
	$(CC) $(CFLAGS) -c y.tab.c

lex.yy.o: lex.yy.c
	$(CC) $(CFLAGS) -c lex.yy.c

main.o: main.c
	$(CC) $(CFLAGS) -c main.c

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

clean:
	rm -f $(TARGET) main.o y.tab.o lex.yy.o y.tab.c y.tab.h lex.yy.c

test: $(TARGET)
	@echo "=== Ожидается успех ==="
	@for f in tests/ok/*.txt; do \
		echo "-- $$f"; ./$(TARGET) "$$f" || exit 1; \
	done
	@echo "=== Ожидается ошибка ==="
	@for f in tests/err/*.txt; do \
		echo "-- $$f"; ./$(TARGET) "$$f" && exit 1 || true; \
	done
	@echo "Все тесты прошли ожидаемо."
