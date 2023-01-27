#include "bits/stdc++.h"
using namespace std;

struct node
{
    int v;
    int w;
    node *next{nullptr};
};

struct heapElement
{
    node n;
    int d;

    bool operator<(const heapElement &other) const
    {
        return d < other.d;
    }

    bool operator>(const heapElement &other) const
    {
        return d > other.d;
    }
};

int main()
{
    ios::sync_with_stdio(0);
    cin.tie(0);

    node teste{0, 0};
    node teste2{1, 1};
    node teste3{2, 2};

    vector<heapElement> v1 = {{teste2, 1}, {teste, 0}, {teste3, 2}};
    make_heap(v1.begin(), v1.end());

    v1.push_back({teste, 4});
    push_heap(v1.begin(), v1.end());

    for (int i = 0; i < 3; i++)
    {
        // cout << "{" << arr[i].n << ", " << arr[i].d << "}" << endl;
        cout << v1[i].n.v << " " << v1[i].n.w << " " << v1[i].d << endl;
    }
    cout << "The maximum element of heap is : ";
    cout << v1.front().d << endl;

    // if (v1[1] < v1[0])
    // {
    //     cout << "comparison works";
    // }
    // else
    // {
    //     cout << "comparison doesn't work";
    // }
}