#include <iostream>
#include <map>

using namespace std;

const map<string, pair<int, int>> COMMANDS = {
	{"forward", {1, 0}},
	{"up",      {0, -1}},
	{"down",    {0, 1}},
};

int main() {
	string cmd;
	int arg, x = 0, y = 0;
	while (cin >> cmd >> arg) {
		x += COMMANDS.at(cmd).first * arg;
		y += COMMANDS.at(cmd).second * arg;
	}
	cout << x * y << endl;
	return 0;
}
