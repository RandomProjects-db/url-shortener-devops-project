#include <stdint.h>

#if defined(__APPLE__)
extern uint64_t _fast_hash(const char *str);
#else
extern uint64_t fast_hash(const char *str);
#endif

uint64_t hash_wrapper(const char *str) {
#if defined(__APPLE__)
    return _fast_hash(str);
#else
    return fast_hash(str);
#endif
}