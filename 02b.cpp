#include <iostream>
#include <map>

using namespace std;

struct op {
	int aim, hor, depth;
};

const map<string, op> COMMANDS = {
	{"forward", op{.hor = 1, .depth = 1}},
	{"up",      op{.aim = -1}},
	{"down",    op{.aim = 1}},
};

int main() {
	string cmd;
	long long arg, x = 0, y = 0, aim = 0;
	while (cin >> cmd >> arg) {
		const op o = COMMANDS.at(cmd);
		aim += o.aim * arg;
		x += o.hor * arg;
		y += o.depth * aim * arg;
	}
	cout << x * y << endl;
	return 0;
}
