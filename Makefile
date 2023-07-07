baa_seminar.py:
	grcc baa_seminar.grc

install:
	sudo cp --preserve=mode *.py /usr/local/bin
	chmod 755 /usr/local/bin/baa_seminar.py
	sudo cp --preserve=mode start_baa /usr/local/bin
	chmod 755 /usr/local/bin/start_baa

clean:
	rm baa_seminar.py
