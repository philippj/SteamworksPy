all:
	gcc -shared -o libsteampy.so -lsteam_api steampy.cpp
clean:
	rm libsteampy.so
install:
	cp libsteampy.so /usr/lib
