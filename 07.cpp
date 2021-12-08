#include <iostream>
#include <cmath>
#include <vector>

using namespace std;

typedef long long ll;

template<typename T> void print(const vector<T>& v) {
	for (auto x : v) {
		cerr << x << " ";
	}
	cerr << endl;
}

vector<ll> position_costs(const vector<int>& input) {
	vector<ll> l(input.size(), 0), r(input.size(), 0);
	for (ssize_t i = 1, j = (ssize_t)input.size() - 2; i < (ssize_t)input.size(); i++, j--) {
		l[i] = l[i - 1] + (ll)i * (input[i] - input[i - 1]);
		r[j] = r[j + 1] + (ll)i * (input[j + 1] - input[j]);
	}

	vector<ll> cost(input.size(), 0);	
	for (size_t i = 0; i < input.size(); i++) {
		cost[i] = l[i] + r[i];
	}

	return cost;
}

ll aprog(int n) {
	return (ll)n * (n + 1) / 2;
}

vector<ll> bruteforce2(const vector<int>& v) {
	vector<ll> res(v[v.size() - 1] - v[0] + 1, 0);
	for (int i = v[0]; i <= v[v.size() - 1]; i++) {
		for (size_t p = 0; p < v.size(); p++) {
			res[i] += aprog(abs(i - v[p]));
		}
	}
	return res;
}

int main() {
	vector<int> input;
	int x;
	while (cin >> x) {
		input.push_back(x);
		char c;
		cin >> c;
	}

	sort(input.begin(), input.end());

	// trying out some funky stuff
	for (auto ct : {make_pair("const", position_costs), make_pair("linear", bruteforce2)}) {
		vector<ll> cost = ct.second(input);
		print(cost);

		size_t best = 0;
		for (size_t i = 0; i < input.size(); i++) {
			if (cost[i] < cost[best]) {
				best = i;
			}
		}

		if (ct.first == string("const")) {
			cout << "Best position with const cost is "
				<< input[best] << ", cost: " << cost[best] << endl;
		} else {
			cout << "Best position with linear cost is "
				<< (input[0] + best) << ", cost: " << cost[best] << endl;
		}
	}

	return 0;
}
