all:
	g++ -shared -fPIC -o libsteampy.so steampy.cpp -lsteam_api 
clean:
	rm libsteampy.so
install:
	cp libsteampy.so /usr/lib
