#include <iostream>
#include <vector>
#include <cassert>
#include <queue>
#include <set>
#include <map>
#include <algorithm>
#include <numeric>

using namespace std;

typedef long long ll;
typedef pair<int, int> point;

vector<point> greater_around(const vector<vector<int>>& inp, int r, int c, int max) {
	vector<point> ret;
	int mid = inp[r][c];
	for (int d = -1; d <= 1; d += 2) {
		if (mid < inp[r+d][c] && inp[r+d][c] <= max) {
			ret.emplace_back(r+d, c);
		}
		if (mid < inp[r][c+d] && inp[r][c+d] <= max) {
			ret.emplace_back(r, c+d);
		}
	}
	return ret;
}

vector<point> greater_around(const vector<vector<int>>& inp, point p, int max) {
	return greater_around(inp, p.first, p.second, max);
}

int get_risk(const vector<vector<int>>& inp, int rows, int cols) {
	int risk = 0;
	for (int i = 1; i <= rows; i++) {
		for (int j = 1; j <= cols; j++) {
			if (greater_around(inp, i, j, 10).size() == 4) {
				//cerr << "low(" << i << ", " << j << ") = " << mid << endl;
				risk += inp[i][j] + 1;
			}
		}
	}
	return risk;
}

ll get_part_two(const vector<vector<int>>& inp, int rows, int cols) {
	set<point> E;
	queue<pair<point, point>> Q;

	map<point, int> size;
	for (int i = 1; i <= rows; i++) {
		for (int j = 1; j <= cols; j++) {
			auto p = make_pair(i, j);
			if (greater_around(inp, p, 10).size() == 4) {
				Q.emplace(p, p);
				E.insert(p);
			}
		}
	}

	while (!Q.empty()) {
		auto p = Q.front();
		Q.pop();
		size[p.second] += 1;

		for (auto next : greater_around(inp, p.first, 8)) {
			if (E.count(next) == 0) {
				E.insert(next);
				Q.emplace(next, p.second);
			}
		}
	}

	vector<pair<int, point>> order;
	for (auto x : size) {
		order.emplace_back(x.second, x.first);
	}
	sort(order.begin(), order.end(), greater<pair<int, point>>());

	assert(order.size() >= 3);
	return accumulate(order.begin(), order.begin() + 3, 1ll, [](ll a, auto b) {
		return a * b.first;
	});
}

int main() {
	vector<string> inp_str;
	string s;
	while (cin >> s) {
		inp_str.push_back(s);
	}

	int rows = (int)inp_str.size(),
	    cols = (int)inp_str[0].size();
	vector<vector<int>> inp(rows + 2, vector<int>(cols + 2, 10));
	{
		int i = 1;
		for (auto s : inp_str) {
			int j = 1;
			for (char c : s) {
				inp[i][j++] = c - '0';
			}
			i++;
		}
	}

	cout << "Risk: " << get_risk(inp, rows, cols) << endl;
	cout << "Basins: " << get_part_two(inp, rows, cols) << endl;
	return 0;
}
