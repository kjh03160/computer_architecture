#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <string.h>

int main(void) {
	FILE* pFile = NULL;
	errno_t err;
	int count;
	unsigned char MEM[80] = {};
	unsigned char data;
	unsigned int IR;
	unsigned int opCode;
	unsigned int opCode_front;
	unsigned int opCode_back;
	unsigned int rs;
	unsigned int rt;
	unsigned int rd;
	unsigned int sh;
	unsigned int offset;
	unsigned int j_address;
	unsigned int funct;
	unsigned int funct_front;
	unsigned int funct_back;
	char opCode_Encode[6][8][10] = {
   {{"R-format"},{"bltz"},{"j"},{"jal"},{"beq"},{"bne"},{""},{""}},
   { {"addi"},{""},{"slti"},{""},{"andi"},{"ori"},{"xori"},{"lui"} },
   { {""},{""},{""},{""},{""},{""},{""},{""} },
   { {""},{""},{""},{""},{""},{""},{""},{""} },
   { {"lb"},{""},{""},{"lw"},{"lbu"},{""},{""},{""} },
   { {"sb"},{""},{""},{"sw"},{""},{""},{""},{""} }
};
	char funct_Encode[6][8][10] = {
   {{"sll"},{""},{"srl"},{"sra"},{""},{""},{""},{""}},
   { {"jr"},{""},{""},{""},{"syscall"},{""},{""},{""} },
   { {"mfhi"},{""},{"mflo"},{""},{""},{""},{""},{""} },
   { {"mul"},{""},{""},{""},{""},{""},{""},{""} },
   { {"add"},{""},{"sub"},{""},{"and"},{"or"},{"xor"},{"nor"} },
   { {""},{""},{""},{"slt"},{""},{""},{""},{""} }
};
	err = fopen_s(&pFile, "as_ex04_fct.bin", "rb");
	if (err) {
		printf("Cannot open file\n");
		return 1;
	}
	int i = 0;
	while (1) {
		count = fread(&data, 1, 1, pFile);
		if (count != 1)
			break;
		MEM[i] = data;	
//		printf("%8x\n", data);
		i++;
		
	}
	MEM[i] = 'k';
	
	fclose(pFile);
	for (i = 0; i<sizeof(MEM); i++){
			if (MEM[i] == 'k'){
				break;
			}
//		printf("%8x", MEM[i]);
		}
	printf("Number of Instructions : %d, Number of Data : %d\n", MEM[3], MEM[7]);
	for (i = 8; i <= MEM[3]*4 + 4;){
		IR = MEM[i]*16*16*16*16*16*16 + MEM[i+1]*16*16*16*16 + MEM[i+2]*16*16 + MEM[i +3];
//		printf("IR : %8x ", IR);
		opCode = IR >>26; // 상위 6비트 
		opCode_front = IR >> 29; // 앞 3비트 
		opCode_back = opCode & 7; // 뒤 3비트
		rs = (IR >> 21) & 31;
		rt = (IR >> 16) & 31;
//		printf("rt1 : %4x\n", (IR >> 21) & 31);
		rd = (IR >> 11) & 31;
		sh = (IR >> 6) & 31;
		offset = IR & 65535;
		j_address = (IR<<6)>>6;
//		printf("%x\n", j_address);
//		printf("opCode : %4x ", opCode);
//		printf("up3(opCode_front) : %2x ", opCode_front); 
//		printf("up3(opCode_back) : %2x ", opCode_back);
		funct = IR & 63; // 하위 6비트
		funct_front = funct >> 3; // 앞 3비트 
		funct_back = funct & 7; // 뒤 3비트 
//		printf("funct : %4x ", funct);
//		printf("down3(funct_front) : %2x ", funct_front);  
//		printf("down3(funct_back) : %2x ", funct_back);
//		printf("Opc : %4x Fct : %4x Inst : %s %s\n", opCode, funct, opCode_Encode[opCode_front][opCode_back],funct_Encode[funct_front][funct_back]); 

		if (strcmp(opCode_Encode[opCode_front][opCode_back], "R-format")){
			if (((opCode_front) == 0) && (opCode_back == 2 || opCode_back == 3)){
				printf("Opc : %4x Fct : %4x Inst : %8s jump address : %7x(26bits) \n", opCode, funct, opCode_Encode[opCode_front][opCode_back], j_address); 
			}
//			else if(((opCode_front) == 0) && ~(opCode_back == 1 || opCode_back == 3)){
//				printf("Opc : %4x Fct : %4x Inst : %s rs : %2x rt : %2x offset : %4x \n", opCode, funct, opCode_Encode[opCode_front][opCode_back], offset); 
//
//			}
			else{
				printf("Opc : %4x Fct : %4x Inst : %8s rs : %4x rt : %4x offset/operand : %4x\n", opCode, funct, opCode_Encode[opCode_front][opCode_back], rs, rt, offset); 

			}

		}
		else{
//			if(((funct_front) == 1) && (funct_back == 0))
//			printf("Opc : %4x Fct : %4x Inst : %8s jump address : %7x(26bits)\n", opCode, funct,funct_Encode[funct_front][funct_back], j_address); 
//			else{
			printf("Opc : %4x Fct : %4x Inst : %8s rs : %4x rt : %4x rd : %4x shamt : %4x \n", opCode, funct, funct_Encode[funct_front][funct_back], rs, rt, rd, sh); 

//			}

		}
		i += 4;
	}
	
	return 0;
}
