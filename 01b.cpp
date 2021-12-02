#include <iostream>
#include <vector>

using namespace std;

typedef long long ll;

int main() {
	vector<ll> depth;
	ll x;
	while (cin >> x) {
		depth.push_back(x);
	}
	const size_t window = 3;
	ll sum = 0;
	for (size_t i = 0; i < depth.size() && i < window; i++) {
		sum += depth[i];
	}
	ll inc = 0;
	for (size_t i = window; i < depth.size(); i++) {
		ll next = sum - depth[i - window] + depth[i];
		if (sum < next) {
			inc++;
		}
		sum = next;
	}
	cout << inc << endl;
	return 0;
}
