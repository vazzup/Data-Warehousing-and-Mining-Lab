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

int main() {
	cout << "Welcome to Vatsal's K Means program!\n";
	cout << "\nEnter the number of datapoints:\n";
	int data_count = 0, mean_count = 0;
	cin >> data_count;
	vector <ll> dataset(data_count), means;
	set <ll> mean_set;
	cout << "Enter the data\n";
	for(int i=0; i<data_count; i++) {
		cin >> dataset[i];
	}
	sort(dataset.begin(), dataset.end());
	cout << "Enter number of means:\n";
	cin >> mean_count;
	vector <ll> cluster[mean_count];
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
			ll min_dist = 100000000000000LL;
			int min_index = -1;
			for(int j=0; j<mean_count; j++) {
				ll dist = max(means[j], dataset[i]) - min(means[j], dataset[i]);
				if(dist < min_dist) {
					min_dist = dist;
					min_index = j;
				}
			}
			cluster[min_index].pb(dataset[i]);
		}
		vector <ll> means_temp;
		for(int i=0; i<mean_count; i++) {
			sort(cluster[i].begin(), cluster[i].end());
			ll mean = 0, sz = cluster[i].size();
			for(int j=0; j<sz; j++) {
				mean += cluster[i][j];
			}
			mean = round((1.0*mean)/sz);
			auto it = lower_bound(cluster[i].begin(), cluster[i].end(), mean);
			int index = it - cluster[i].begin();
			if(index == sz) index--;
			else if(index > 0) {
				if(abs(cluster[i][index - 1] - mean) < abs(cluster[i][index] - mean)) {
					index--;
				}
			}
			means_temp.pb(cluster[i][index]);
			if(cluster[i][index] != means[i]) {
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
	cout << "The Clusters are... \n";
	for(int i=0; i<mean_count; i++) {
		for(int j=0; j<cluster[i].size(); j++) {
			cout << cluster[i][j] << " ";
		}
		cout << "with mean " << means[i] << "\n";
	}
	return 0;
}
