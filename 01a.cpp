#include <iostream>

using namespace std;

typedef long long ll;

int main() {
	bool first = true;
	ll x, last, inc = 0;
	while (cin >> x) {
		if (!first && last < x) {
			inc++;
		}
		first = false;
		last = x;
	}
	cout << inc << endl;
	return 0;
}
