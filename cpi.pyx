# Example: monte_carlo_pi_cython.pyx
cimport cython
from libc.stdlib cimport rand, RAND_MAX

@cython.boundscheck(False)
@cython.wraparound(False)
def monte_carlo_pi_simulation_cython(int samples):
    cdef int i, inside_circle = 0
    cdef double x, y
    for i in range(samples):
        x = rand() / RAND_MAX
        y = rand() / RAND_MAX
        if x * x + y * y <= 1:
            inside_circle += 1
    return (4.0 * inside_circle) / samples
