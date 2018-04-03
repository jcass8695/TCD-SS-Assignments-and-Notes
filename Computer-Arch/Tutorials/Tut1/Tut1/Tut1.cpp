// Tut1.cpp : Defines the entry point for the console application.
// Jack Cassidy SS Engineering 03/10/2017
// Student No. 1432 0816

#include "stdafx.h"
#include "assert.h"
#include "fib32.h"
#include "t1.h"
#include "iostream"

using namespace std;

int main()
{	
	cout << "min(21, 3, 14)" << endl;
	assert(min(21, 3, 14) == 3);
	cout << "PASS" << endl;

	cout << "p(8, 9, 3, 2)" << endl; 
	assert(p(8, 9, 3, 2) == 2);
	cout << "PASS" << endl;

	cout << "p(0, 1, 3, 2)" << endl;
	assert(p(0, 1, 3, 2) == 0);
	cout << "PASS" << endl;

	cout << "gcd(21, 14)" << endl;
	assert(gcd(21, 14) == 7);
	cout << "PASS" << endl;

	cout << "gcd(14, 21)" << endl;
	assert(gcd(14, 21) == 7);
	cout << "PASS" << endl;

	cout << "gcd(5, 3)" << endl;
	assert(gcd(5, 3) == 1);
	cout << "PASS" << endl;

	cout << "gcd(3, 5)" << endl;
	assert(gcd(3, 5) == 1);
	cout << "PASS" << endl;

	cout << "gcd(8, 6)" << endl;
	assert(gcd(8, 6) == 2);
	cout << "PASS" << endl;

	cout << "gcd(6, 8)" << endl;
	assert(gcd(6, 8) == 2);
	cout << "PASS" << endl;

	cout << "gcd(-2, 4)" << endl;
	assert(gcd(-2, 4) == 2);
	cout << "PASS" << endl;

	getchar();
	return 0;
}
