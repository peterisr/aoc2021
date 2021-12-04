#include <iostream>
#include <vector>
#include <sstream>

using namespace std;

typedef vector<vector<int>> vvi;

class Board {
	private:
		vvi data;
		size_t n;
		vvi marked;
		vector<int> mr, mc;
		int sum;
		bool had_bingo;

	public:
		Board(const vvi& data_) 
			: data(data_),
		          n(data_.size()),
			  marked(n, vector<int>(n, 0)),
			  mr(n, 0),
			  mc(n, 0),
		   	  sum(0),
			  had_bingo(false) {
			for (size_t r = 0; r < n; r++) {
				for (size_t c = 0; c < n; c++) {
					sum += data[r][c];
				}
			}
		
		};

		// returns score, if bingo is hit with current num; -1 otherwise
		int mark(int num) {
			int res = -1;
			for (size_t r = 0; !had_bingo && r < n; r++) {
				for (size_t c = 0; !had_bingo && c < n; c++) {
					if (data[r][c] == num && !marked[r][c]) {
						marked[r][c] = 1;
						sum -= num;
						mr[r]++;
						mc[c]++;
						if (mr[r] == (int)n || mc[c] == (int)n) {
							res = sum * num;
						}
					}
				}
			}

			if (res >= 0) {
				had_bingo = true;
			}

			return res;
		}
};

int main() {
	string ln;
	getline(cin, ln);
	stringstream ss(ln);
	vector<int> calls;
	int x;
	while (ss >> x) {
		calls.push_back(x);
		char comma;
		ss >> comma;
	}

	vector<Board> boards;
	const int board_size = 5;
	vvi data(board_size, vector<int>(board_size));
	while (cin >> data[0][0]) {
		for (int r = 0; r < board_size; r++) {
			for (int c = (r == 0 ? 1 : 0); c < board_size; c++) {
				cin >> data[r][c];
			}
		}

		boards.push_back(Board(data));
	}

	cerr << "Read " << boards.size() << " boards" << endl;

	int first = -1, last = -1;
	for (int call : calls) {
		for (auto &board : boards) {
			int bingo = board.mark(call);
			if (bingo != -1) {
				if (first == -1) {
					first = bingo;
				}
				last = bingo;
			}
		}
	}

	cout << "Score of first winner: " << first << endl;
	cout << "Score of last winner: " << last << endl;

	return 1;
}
