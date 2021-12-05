#include <stdio.h>
#include <vector>
#include <map>

using namespace std;

struct line {
	int x1, y1, x2, y2;
};

int sign(int x) {
	if (x == 0) {
		return 0;
	}
	return x > 0 ? 1 : -1;
}

int on(int x, int x1, int x2) {
	return min(x1, x2) <= x && x <= max(x1, x2);
}

vector<pair<int, int>> enumerate(const line& l, const string& type) {
	vector<pair<int, int>> r;

	int xdiff = sign(l.x2 - l.x1), ydiff = sign(l.y2 - l.y1);
	if ((type == "hv" && abs(xdiff) + abs(ydiff) == 1) || type == "hvd") {
		for (
			int x = l.x1, y = l.y1;
			on(x, l.x1, l.x2) && on(y, l.y1, l.y2);
			x += xdiff, y += ydiff
		) {
			r.emplace_back(x, y);
		}
	}

	return r;
}

int main() {
	vector<line> lines;
	line l;
	while (scanf("%d,%d -> %d,%d", &l.x1, &l.y1, &l.x2, &l.y2) == 4) {
		lines.push_back(l);
	}

	for (const auto& type : {"hv", "hvd"}) {
		map<pair<int, int>, int> count;
		for (auto l : lines) {
			for (auto p : enumerate(l, type)) {
				count[p] += 1;
			}
		}

		int ans = 0;
		for (auto it : count) {
			if (it.second >= 2) {
				ans++;
			}
		}

		printf("At least 2 lines overlap in %d points (type = %s)\n", ans, type);
	}

	return 0;
}
