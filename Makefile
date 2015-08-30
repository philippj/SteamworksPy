makeall:
	gcc -o SteamworksPy.so -shared -fPIC steampy.cpp -lsteam_api 
clean:
	rm SteamworksPy.so
