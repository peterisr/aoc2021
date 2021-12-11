#include <iostream>
#include <stack>
#include <map>
#include <algorithm>
#include <vector>
#include <cassert>

using namespace std;

typedef long long ll;

const map<char, int> CORRUPT_SCORES = {
	{')', 3},
	{']', 57},
	{'}', 1197},
	{'>', 25137},
};

const map<char, int> INCOMPLETE_SCORES = {
	{')', 1},
	{']', 2},
	{'}', 3},
	{'>', 4},
};

const map<char, char> OTHER = {
	{'(', ')'},
	{'[', ']'},
	{'{', '}'},
	{'<', '>'},

	{')', '('},
	{']', '['},
	{'}', '{'},
	{'>', '<'},
};

pair<int, ll> get_score(const string& line) {
	int corrupted = 0;

	stack<char> s;
	for (char c : line) {
		if (CORRUPT_SCORES.count(c) == 0) { // c - opening
			s.push(c);
		} else { // c - closing
			if (OTHER.at(c) != s.top()) {
				corrupted += CORRUPT_SCORES.at(c);
				break;
			}

			s.pop();
		}
	}

	ll incomplete = 0;
	if (corrupted == 0) {
		// incomplete line
		while (!s.empty()) {
			char c = OTHER.at(s.top());
			incomplete *= 5;
			incomplete += INCOMPLETE_SCORES.at(c);
			s.pop();
		}
	}

	return make_pair(corrupted, incomplete);
}

int main() {
	int corrupted = 0;
	string line;
	vector<ll> incomplete;
	while (cin >> line) {
		auto score = get_score(line);
		corrupted += score.first;
		if (score.second > 0) {
			incomplete.push_back(score.second);
		}
	}

	sort(incomplete.begin(), incomplete.end());
	assert(incomplete.size() % 2 == 1);

	cout << "Score corrupted: " << corrupted << endl;
	cout << "Score incomplete: " << incomplete[incomplete.size()/2] << endl;
	return 0;
}
