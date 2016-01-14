makeall:
	g++ -o SteamworksPy.so -shared -fPIC SteamworksPy.cpp -lsteam_api 
clean:
	rm SteamworksPy.so
