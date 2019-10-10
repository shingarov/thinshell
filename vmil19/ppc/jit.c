#include <stdint.h>

uint32_t nZoneBuffer[32];
void *nZone = &nZoneBuffer[0];

void generateLis(uint32_t *instr, uint16_t x) {
	*instr = ( 0b0011110001100000 << 16 )
	         //  <opcd>_RT=3_RA=0
			| x;
}

void generateOri(uint32_t *instr, uint16_t x) {
	*instr = ( 0b0110000001100011 << 16 )
	         //  <opcd>_RS=3_RA=3
			| x;
}

void loadConstant(uint32_t x) {
	uint32_t hi = (x >> 16) & 0x0000FFFF;
	uint32_t lo = x         & 0x0000FFFF;
	generateLis(&nZoneBuffer[0], hi);
	generateOri(&nZoneBuffer[1], lo);
}

int main(int arg1, char **_) {
	uint32_t x = arg1;
//	uint32_t x = 0x12345678;
	loadConstant(x);
	goto *nZone;
	return 0;
}

