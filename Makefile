baa_seminar.py:
	grcc baa_seminar.grc

install:
	sudo cp --preserve=mode *.py /usr/local/bin
	chmod 755 /usr/local/bin/baa_seminar.py

clean:
	rm baa_seminar.py
