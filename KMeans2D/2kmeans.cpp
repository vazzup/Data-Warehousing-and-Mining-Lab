#include <iostream>
#include <cstdio>
#include <cmath>
#include <vector>
#include <set>
#include <ctime>
#include <cstdlib>
#include <algorithm>

#define ll long long
#define pb push_back
#define mp make_pair
#define F first
#define S second

using namespace std;

double get_dist(pair<ll, ll> a, pair<ll, ll> b);

int main() {
	cout << "Welcome to Vatsal's K Means program!\n";
	cout << "\nEnter the number of datapoints:\n";
	int data_count = 0, mean_count = 0;
	cin >> data_count;
	vector < pair<ll, ll> > dataset(data_count), means;
	set < pair<ll, ll> > mean_set;
	cout << "Enter the data\n";
	for(int i=0; i<data_count; i++) {
		cin >> dataset[i].F >> dataset[i].S;
	}
	sort(dataset.begin(), dataset.end());
	cout << "Enter number of means:\n";
	cin >> mean_count;
	vector < pair<ll, ll> > cluster[mean_count];
	cout << "Computing the means...\n";
	srand(time(NULL));
	for(int i=0; i<mean_count; i++) {
		int index =  rand() % data_count;
		while(mean_set.find(dataset[index]) != mean_set.end()) {
			index = rand() % data_count;
		}
		means.pb(dataset[index]);
		mean_set.insert(dataset[index]);
	}
	while(true) {
		bool changed = false;
		for(int i=0; i<mean_count; i++) {
			cluster[i].clear();
		}
		for(int i=0; i<data_count; i++) {
			double min_dist = 1e15;
			int min_index = -1;
			for(int j=0; j<mean_count; j++) {
				double dist = get_dist(means[j], dataset[i]);
				if(dist < min_dist) {
					min_dist = dist;
					min_index = j;
				}
			}
			cluster[min_index].pb(dataset[i]);
		}
		vector < pair<ll, ll> > means_temp;
		for(int i=0; i<mean_count; i++) {
			sort(cluster[i].begin(), cluster[i].end());
			ll sz = cluster[i].size();
			pair<ll, ll> mean = mp(0, 0);
			for(int j=0; j<sz; j++) {
				mean.F += cluster[i][j].F;
				mean.S += cluster[i][j].S;
			}
			mean.F = round((1.0*mean.F)/sz);
			mean.S = round((1.0*mean.S)/sz);
			/*auto it = lower_bound(cluster[i].begin(), cluster[i].end(), mean);
			int index = it - cluster[i].begin();
			if(index == sz) index--;
			else if(index > 0) {
				if(get_dist(cluster[i][index - 1], mean) < get_dist(cluster[i][index], mean)) {
					index--;
				}
			}
			means_temp.pb(cluster[i][index]);*/
			double min_dist = 1e14;
			int min_index = -1;
			for(int j=0; j<sz; j++) {
				double dist = get_dist(cluster[i][j], means[i]);
				if(dist < min_dist) {
					min_dist = dist;
					min_index = j;
				}
			}
			means_temp.pb(cluster[i][min_index]);
			if(cluster[i][min_index] != means[i]) {
				changed =  true;
			}
		}
		for(int i=0; i<mean_count; i++) {
			means[i] = means_temp[i];
		}
		if(!changed) {
			break;
		}
	}
	cout << "Clusters calculated using K Means!\n";
	cout << "The Clusters are:\n";
	for(int i=0; i<mean_count; i++) {
		for(int j=0; j<cluster[i].size(); j++) {
			cout << cluster[i][j].F << "," << cluster[i][j].S << " ";
		}
		cout << "with mean " << means[i].F << "," << means[i].S << "\n";
	}
	return 0;
}

double get_dist(pair<ll, ll> a, pair<ll, ll> b) {
	return sqrt(pow(a.F - b.F, 2) 
				+ pow(a.S - b.S, 2));
}
