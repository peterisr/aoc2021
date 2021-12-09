#include <iostream>
#include <cassert>
#include <bitset>
#include <vector>
#include <map>

using namespace std;

typedef long long ll;

int uniq_letters(const string& s) {
	bitset<26> bs;
	for (char c : s) {
		bs.set(c - 'a');
	}
	return (int)bs.count();
}

const int SEGMENTS = 7;
const vector<string> DIGITS = {
	"abcefg",  // 0
	"cf",      // 1
	"acdeg",   // 2
	"acdfg",   // 3
	"bcdf",    // 4
	"abdfg",   // 5
	"abdefg",  // 6
	"acf",     // 7
	"abcdefg", // 8
	"abcdfg",  // 9

	// a - 8 
	// b - 6 - UNIQ!
	// c - 8
	// d - 7
	// e - 4 - UNIQ!
	// f - 9 - UNIQ!
	// g - 7
};

int uniq_idx(const string& s) {
	int lc = uniq_letters(s);
	if (lc == 5 || lc == 6) {
		return -1;
	}

	for (int i = 0; i < (int)DIGITS.size(); i++) {
		if (lc == (int)DIGITS[i].size()) {
			return i;
		}
	}

	assert(false);
}

int decode(const vector<string>& l, const vector<string>& r) {
	// strategy 1: letter frequency
	vector<int> letter_stats(SEGMENTS, 0);
	for (const auto& s : l) {
		for (char c : s) {
			letter_stats[c - 'a']++;
		}
	}

	map<char, char> found;
	for (auto x : {make_pair(4, 'e'), make_pair(6, 'b'), make_pair(9, 'f')}) {
		for (int i = 0; i < SEGMENTS; i++) {
			if (letter_stats[i] == x.first) {
				found[(char)('a' + i)] = x.second;
			}
		}
	}
	assert(found.size() == 3);

	// strategy 2: deduction
	while (SEGMENTS > (int)found.size()) {
		for (const auto& s : l) {
			string unknown = "";
			for (char c : s) {
				if (found.count(c) == 0) {
					unknown += c;
				}
			}

			if (unknown.size() != 1) {
				continue;
			}

			char uk = unknown[0];
			if (s.size() == 2) {
				// 1
				found[uk] = 'c';
			} else if (s.size() == 3) {
				// 7
				found[uk] = 'a';
			} else if (s.size() == 4) {
				// 4
				found[uk] = 'd';
			} else if (s.size() == 7) {
				// 8
				found[uk] = 'g';
			}
		}
	}

	int ret = 0;
	for (auto s : r) {
		string real = "";
		for (char c : s) {
			real += found.at(c);
		}
		sort(real.begin(), real.end());

		auto pos = find(DIGITS.begin(), DIGITS.end(), real);
		assert(pos != DIGITS.end());

		int digit = distance(DIGITS.begin(), pos);
		ret = ret * 10 + digit;
	}

	return ret;
}

int main() {
	vector<pair<vector<string>, vector<string>>> input;
	string s;
	while (cin >> s) {
		vector<string> l, r;
		l.push_back(s);
		for (int i = 1; i < 10; i++) {
			cin >> s;
			l.push_back(s);
		}

		cin >> s;
		assert(s == string("|"));

		for (int i = 0; i < 4; i++) {
			cin >> s;
			r.push_back(s);
		}

		input.emplace_back(l, r);
	}

	int cnt1478 = 0;
	for (const auto& pair : input) {
		for (const auto &w : pair.second) {
			if (uniq_idx(w) != -1) {
				cnt1478++;
			}
		}
	}

	cout << "Number of digit 1, 4, 7, 8 occurrences: " << cnt1478 << endl;

	int sum = 0;
	for (const auto& pair : input) {
		sum += decode(pair.first, pair.second);
	}

	cout << "Sum of all numbers: " << sum << endl;
	return 0;
}
