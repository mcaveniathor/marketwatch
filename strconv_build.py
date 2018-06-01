#!/usr/bin/python3
from cffi import FFI
ffibuilder = FFI()
ffibuilder.set_source("_strconv",
        r"""
            #include <stdlib.h>

            int strToInt(char *input) {
                return (int) strtol(input, NULL, 10);
            }
            double strToFloat(char *input) {
                return strtod(input, NULL);
            }

            struct data parseData(struct d) {
                struct data ret;
                //Binance
                if(d.exchange == 1) {
                }

            }
        """,
        libraries = [])
ffibuilder.cdef("""
    int strToInt(char *input);
    double strToFloat(char *input);
    struct data {
        
    }
    """)
if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
