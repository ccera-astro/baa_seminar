baa_seminar.py:
	grcc baa_seminar.grc
	chmod 755 baa_seminar.py

install:
	sudo cp --preserve=mode *.py /usr/local/bin

clean:
	rm baa_seminar.py
