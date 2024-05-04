# distutils: language = c
# cython: language_level=3, linetrace=True, binding=True

cdef class ScoringMatrix:
    cdef readonly str name
    cdef readonly str alphabet

    cdef size_t        _size
    cdef size_t        _nitems
    cdef Py_ssize_t[2] _shape

    cdef float*  _data
    cdef float** _matrix

    cdef int _allocate(self, size_t length) except 1 nogil

    cdef const float* data(self) except NULL nogil
    cdef const float** matrix(self) except NULL nogil    

    cpdef bint is_integer(self)
    cpdef float min(self)
    cpdef float max(self)
    cpdef ScoringMatrix copy(self)
    cpdef ScoringMatrix shuffle(self, str alphabet)