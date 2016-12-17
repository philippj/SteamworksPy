makeall:
	g++ -std=c++11 -o SteamworksPy.so -shared -fPIC SteamworksPy.cpp -lsteam_api 
clean:
	rm SteamworksPy.so
