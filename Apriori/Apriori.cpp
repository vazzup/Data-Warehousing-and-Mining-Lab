#include <iostream>
#include <cstdio>
#include <vector>
#include <algorithm>
#include <set>
#include <map>
#include <unordered_map>
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

void apriori(vector < vector <ll> > &t, ll threshold);

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
	ll n;
	vector < vector <ll> > t;
	cout << "Enter the number of test tuples\n";
	cin >> n;
	t.resize(n);
	for(ll i=0; i < n; i++) {
		ll c = 0;
		cin >> c;
		t[i].resize(c);
		for(ll j=0; j<c; j++) {
			cin >> t[i][j];
		}
	}
	return 0;
}

void apriori(vector < vector <ll> > &t, ll threshold) {
	unordered_map < vector <ll> , ll> c;
	ll depth = 1;
	while(true) {
		
	}
}
