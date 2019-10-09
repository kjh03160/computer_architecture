#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>

int addSubtract(int X, int Y, int C) {
	int ret;
	if (C < 0 || C > 1) {
		printf("error in add/subtract operation\n");
		exit(1);
	}
	if (C == 0) {
		ret = X + Y;
	}
	else {
		ret = X - Y;
	}
	return ret;
}

int logicOperation(int X, int Y, int C) {
	if (C < 0 || C > 3) {
		printf("error in logic operation\n");
		exit(1);
	}
	if (C == 0) {
		return X & Y;
	}
	else if (C == 1) {
		return X | Y;
	}
	else if (C == 2) {
		return X ^ Y;
	}
	else {
		return ~(X | Y);
	}
}

int shiftOperation(int V, int Y, int C) {
	int ret, x;
	x = V & 31; // 끝 5bit 추출
	if (C < 0 || C > 3) {
		printf("error in shift operation\n");
		exit(1);
	}
	if (C == 0) {
		ret =  Y;
	}
	else if (C == 1) { // 일반 논리 시프트를 구현해야함
		ret = (Y << x);
	}
	else if (C == 2) { 
		const size_t int_bits = sizeof(int) * 8; // 32비트
		unsigned int mask = (1u << x) - 1;	// 1u = 0이 31개, 1이 끝에 한개 / x에 따라 1을 더 만들거나 위치 조정
		mask = mask << (int_bits - x);      // 1들을 맨 앞에서부터 x개 배치
											// NOT 사용하여 0과 1 변환하여 맨 앞에서부터 x개 0 만들고 나머지 1을 만들어 
		Y = ((Y >> x) | mask) & ~mask;						// 이 부분에서 MSB는 0으로 만들고 나머지 부분은 1과 &연산으로 본래의 값 반환
		ret = Y;
	}
	else { // 산술 시프트는 컴파일러가 자동으로 해줌
			ret = Y >> x;
	}
	return ret;
}

int checkZero(int S) {
	int ret;
	if (S == 0) {	
		ret = 1;
	}
	else {
		ret =  0;
	}
	return ret;
}

int checkSetLess(int X, int Y) {
	int ret;
	if (X < Y) {
		ret = 1;
	}
	else {
		ret = 0;
	}
	return ret;
}

int ALU(int X, int Y, int C, int* Z) {
	int c32, c10;
	int ret;
	
	c32 = (C >> 2) & 3;
	c10 = C & 3;
	if (c32 == 0) {
		ret = shiftOperation(X, Y, c10);
	}
	else if (c32 == 1) {
		ret = checkSetLess(X, Y);
	}
	else if (c32 == 2) {
		c10 = C & 1;
		ret = addSubtract(X, Y, c10);
		*Z = checkZero(ret);
	}
	else {
		ret = logicOperation(X, Y, c10);
	}
	return ret;
}

void test(void) {
	int x, y, i, s, z;
	scanf("%d %d", &x, &y);
	printf("x: %8x, y: %8x\n", x, y);
	for (i = 0; i < 16; i++) {
		s = ALU(x, y, i, &z);
		printf("s: %8x, z: %8x\n", s, z);
	}
	return;
}


int main(void) {
	test();
	return 0;
}