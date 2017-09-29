#include <iostream>
#include <cstdio>
#include <vector>
#include <algorithm>
#include <set>
#include <map>
#include <cmath>

#define ll long long int
#define pll pair<long long, long long>
#define pii pair<int, int>
#define pb push_back
#define mp make_pair
#define getchar_unlocked getchar
#define F first
#define S second
#define MOD 1000000007

using namespace std;

string read_till_comma();

int main() {
	int num_cols, num_data;
	cout << "Enter the number of columns and the number of datarows\n";
	cin >> num_cols >> num_data;
	vector < vector <string> > data(num_data);
	vector < set <string> > unique_items(4);
	vector < map< pair<string, string>, double> > prob(num_data);
	cout << "Enter the datarows on seperate lines as comma seperated values..\n";
	for(int i = 0; i < num_data; i++) {
		for(int j = 0; j < num_cols; j++) {
			string s = read_till_comma();
			// cout << s << " read on line " << i << " column " << j << "\n";
			data[i].pb(s);
			unique_items[j].insert(s);
		}
	}
	cout << "Calculating probabilities...\n";
	for(int i = 0; i < num_cols - 1; i++) {
		for(auto x : unique_items[i]) {
			for(auto y : unique_items[num_cols - 1]) {
				// cout  << "calculating for " << x << " " << y << "\n";
				for(int l = 0; l < data.size(); l++) {
					if((data[l][i]) == x && (data[l][num_cols - 1] == y)) {
						prob[i][mp(x, y)]++;
					}
				}
				// cout << "The count for " << x << "& " << y << " is " << prob[i][mp(x, y)] << "\n";
			}
			for(auto y : unique_items[num_cols - 1]) {
				prob[i][mp(x, y)] /= (num_data*1.0);
				// cout << prob[i][mp(x, y)] << "\n";
			}
		}
	}
	cout << "Enter number of queries...\n";
	int q;
	cin >> q;
	for(int i = 0; i < q; i++) {
		vector <string> query(num_cols - 1);
		for(int j = 0; j < num_cols - 1; j++) {
			query[j] = read_till_comma();
			// cout <<  query[j] << ",";
		}
		// cout << "\n";
		double ans = 1, mans = -1;
		string sans = "";
		for(auto x : unique_items[num_cols - 1]) {
			ans = 1;
			for(int k = 0; k < num_cols - 1; k++) {
				ans *= prob[k][mp(query[k], x)];
			}
			cout << "Probability of getting classified as " << x << " is " << ans << "\n";
			if(ans > mans) {
				mans = ans;
				sans = x;
			}
		}
		cout << "Hence, this query is classified as: " << sans << "\n";
	}
	return 0;
}

string read_till_comma() {
	int c;
	string s = "";
	// cout << "called...\n";
	while((c = getchar()) == ' ' || c == '\n' || c == '\t' || c == ',');
	while(c != ',' && c != ' ' && c != '\n' && c != '\t' && c != EOF) {
		s += c;
		// cout  << (char)c << " read...\n";
		c = getchar();
	}
	// cout << "Exiting...\n";
	return s;
}
