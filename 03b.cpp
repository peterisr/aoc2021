#include <iostream>
#include <algorithm>
#include <vector>
#include <cassert>

using namespace std;

long long bin2dec(const string& s) {
	long long res = 0;
	for (char c : s) {
		res *= 2;
		res += c - '0';
	}
	return res;
}

long long find(const vector<string>& values, int common) {
	auto l = values.begin(), r = values.end();
	size_t pos = 0, sz = distance(l, r);
	while (sz > 0) {
		// kinda implied by problem statement
		assert(*l != *r);

		size_t mc_pos = sz / 2 + (sz % 2 == 0);
		auto most_common = l + mc_pos;
		char go;

		if (common) {
			go = (*most_common)[pos];
		} else {
			go = ((*most_common)[pos] == '0' ? '1' : '0');
		}

		auto first_1 = upper_bound(l, r, '0', [pos](char c, const string& s) { 
			return c < s[pos];
		});

		if (go == '0') {
			r = prev(first_1);
		} else {
			l = first_1;
		}

		sz = distance(l, r);
		pos++;
	}
	return bin2dec(*l);
}

int main() {
	vector<string> values;
	string x;
	while (cin >> x) {
		values.push_back(x);
	}

	sort(values.begin(), values.end());
	long long oxigen = find(values, 1);
	long long co2 = find(values, 0);
	long long res = oxigen * co2;
	cout << res << endl;
	return 0;
}
