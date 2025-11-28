CC = gcc
CFLAGS = -O2 -Wall
TARGET = winpatable
SRC = launcher.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

install: $(TARGET)
	mkdir -p /app/bin
	cp $(TARGET) /app/bin/

clean:
	rm -f $(TARGET)
