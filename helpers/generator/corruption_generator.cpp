#include "sram.cpp"

#include <cstdio>
#include <cstdlib>

int main(int argc, char **argv){
    SRAM_Corruption hexC6;
    hexC6.loadInitialState("sram_start.dmp");
    hexC6.loadSpriteBehavior("behavior_c6.txt");
    SRAM_Corruption hexDC;
    hexDC.loadInitialState("sram_start.dmp");
    hexDC.loadSpriteBehavior("behavior_dc.txt");
    uint8 *output;
    for (int i=1; i<argc; i++){
        int iters = atoi(argv[i]);
        if (i % 2 == 1){
            hexC6.loadInitialState(hexDC.sram, SRAM_SIZE);
            while (iters--) hexC6.corrupt();
            output = hexC6.sram;
        }else{
            hexDC.loadInitialState(hexC6.sram, SRAM_SIZE);
            while (iters--) hexDC.corrupt();
            output = hexDC.sram;
        }
    }
    FILE *fp = fopen("sram_final.dmp", "wb");
    fwrite(output, 1, 0x2000, fp);
    fclose(fp);
}
