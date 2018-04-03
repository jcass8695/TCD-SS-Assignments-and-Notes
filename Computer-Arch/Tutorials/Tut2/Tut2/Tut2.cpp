// Tut 2
// Jack Cassidy
// Student No. 1432 0816

#include "stdafx.h"	
#include "stdio.h"
#include <iostream>
#include <assert.h>
#include "assembly-tut2.h"	

using namespace std;


int main() {
	cout << "---- minX64(__int64 a, __int64 b, __int64 c) returns minimum of 3 numbers ----" << endl;

	cout << "minX64(1, -2, 3) == -2" << endl;
	assert(minX64(1, -2, 3) == -2);
	cout << "PASS" << endl;

	cout << "minX64(21, 7, 5) == 5" << endl;
	assert(minX64(21, 7, 5) == 5);
	cout << "PASS" << endl;

	cout << "---- pX64(__int64 i, __int64 j, __int64 k, __int64 l) returns minimum of 4 numbers and the global const g = 4 ----" << endl;

	cout << "pX64(1, 2, 3, 4) == 1" << endl;
	assert(pX64(1, 2, 3, 4) == 1);
	cout << "PASS" << endl;
	
	cout << "pX64(-1, 2, 3, -4) == -4" << endl;
	assert(pX64(-1, 2, 3, -4) == -4);
	cout << "PASS" << endl;
	
	cout << "pX64(11, 12, 13, 14) == 4" << endl;
	assert(pX64(11, 12, 13, 14) == 4);
	cout << "PASS" << endl;


	cout << "---- gcdX64(__int64 a, __int64 b) returns greatest common denominator of 2 numbers ----" << endl;
	cout << "gcdX64(6, 14) == 2" << endl;
	assert(gcdX64(6, 14) == 2);
	cout << "PASS" << endl;

	cout << "gcdX64(14, 6) == 2" << endl;
	assert(gcdX64(14, 6) == 2);
	cout << "PASS" << endl;

	cout << "gcdX64(2, 15) == 1" << endl;
	assert(gcdX64(2, 15) == 1);
	cout << "PASS" << endl;

	cout << "gcdX64(2, -2) == 2" << endl;
	assert(gcdX64(2, -2) == 2);
	cout << "PASS" << endl;

	cout << "gcdX64(-2, 2) == 2" << endl;
	assert(gcdX64(-2, 2) == 2);
	cout << "PASS" << endl;

	cout << "gcdX64(-2, -2) == 2" << endl;
	assert(gcdX64(-2, -2) == 2);
	cout << "PASS" << endl;

	cout << "gcdX64(1, 51)" << endl;
	assert(gcdX64(1, 51) == 1);
	cout << "PASS" << endl;

	cout << "gcdX64(1, -51)" << endl;
	assert(gcdX64(1, -51) == 1);
	cout << "PASS" << endl;

	cout << "gcdX64(51, 1)" << endl;
	assert(gcdX64(51, 1) == 1);
	cout << "PASS" << endl;

	cout << "Calling qx64(1, 2, 3, 4, 5)" << endl;
	qX64(1, 2, 3, 4, 5);

	cout << endl << "Calling qx64(1, 2, 3, 4, 5) with no shadow space allocated" << endl;
	qX64_no_shadow(1, 2, 3, 4, 5);
	cout << endl;
	getchar();

	return 0;

}
