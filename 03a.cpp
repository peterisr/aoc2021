#include <iostream>
#include <vector>
#include <cassert>
#include <algorithm>

using namespace std;

int main() {
	vector<vector<int>> cnt(2, vector<int>(20, 0));
	string x;
	ssize_t maxlen = 0;
	while (cin >> x) {
		reverse(x.begin(), x.end());
		ssize_t p = 0;
		for (char c : x) {
			cnt[c - '0'][p++]++;
		}
		maxlen = max(maxlen, p);
	}

	long long gamma = 0, epsilon = 0;
	ssize_t i = maxlen - 1;
	while (i >= 0) {
		assert(cnt[0][i] != cnt[1][i]);
		gamma *= 2;
		epsilon *= 2;
		if (cnt[1][i] > cnt[0][i]) {
			gamma += 1;
		} else {
			epsilon += 1;
		}
		i--;
	}

	long long res = gamma * epsilon;	
	cout << res << endl;
	return 0;
}
