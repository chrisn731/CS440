all: filter.so

filter.so: filter.c
	gcc -O2 -shared -fPIC $^ -o $@

clean:
	rm -f filter.so *.pyc
