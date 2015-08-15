make-lin:
	gcc -o libsteampy.so -shared -fPIC steampy.cpp -lsteam_api 
make-win:
	# not made yet
make-mac:
	# not made yet
clean:
	rm libsteampy.so