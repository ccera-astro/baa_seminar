baa_seminar.py: baa_seminar.grc
	grcc baa_seminar.grc

install:
	cp --preserve=mode *.py /usr/local/bin
	chmod 755 /usr/local/bin/baa_seminar.py
	cp --preserve=mode start_baa /usr/local/bin
	chmod 755 /usr/local/bin/start_baa
	mkdir -p /usr/local/share/icons
	cp satellite-dish-svgrepo-com.svg /usr/local/share/icons
	chmod 644 /usr/local/share/icons/satellite-dish-svgrepo-com.svg
	

clean:
	rm baa_seminar.py
