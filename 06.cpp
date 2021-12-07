#include <iostream>
#include <numeric>
#include <vector>

using namespace std;

typedef long long ll;

const int NEW_FISH = 8;
const int RESET_FISH = 6;
const int STATES = NEW_FISH + 1;

vector<ll> to_state(const vector<int>& input) {
	vector <ll> state(STATES, 0);
	for (int x : input) {
		state[x]++;
	}
	return state;
}

vector<ll> iterate(const vector<ll>& state, int days) {
	vector<ll> end(state);
	while (days--) {
		ll zero = end[0];
		for (int i = 1; i < STATES; i++) {
			end[i - 1] = end[i];
		}
		end[NEW_FISH] = zero;
		end[RESET_FISH] += zero;
	}
	return end; 
}

ll ans(const vector<ll>& init_state, int days) {
	vector<ll> end_state = iterate(init_state, days);
	return accumulate(end_state.begin(), end_state.end(), 0ll);
}

int main() {
	vector<int> input;
	int x;
	while (cin >> x) {
		input.push_back(x);
		char c;
		cin >> c;
	}

	vector<ll> init_state = to_state(input);
	for (int days : {80, 256}) {
		cout << "After " << days << " -> " << ans(init_state, days) << endl;
	}

	return 0;
}
