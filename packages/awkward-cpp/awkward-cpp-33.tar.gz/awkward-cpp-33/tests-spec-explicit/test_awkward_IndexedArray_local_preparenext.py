import pytest
import numpy
import kernels

def test_awkward_IndexedArray_local_preparenext_1():
	tocarry = [123, 123, 123, 123, 123]
	nextlen = 4
	nextparents = [0, 0, 0, 0]
	parentslength = 5
	parents = [0, 0, 0, 0, 0]
	starts = [0]
	funcPy = getattr(kernels, 'awkward_IndexedArray_local_preparenext')
	funcPy(tocarry = tocarry,nextlen = nextlen,nextparents = nextparents,parentslength = parentslength,parents = parents,starts = starts)
	pytest_tocarry = [0, 1, 2, 3, -1]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_local_preparenext_2():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextlen = 7
	nextparents = [0, 0, 0, 0, 1, 1, 1]
	parentslength = 11
	parents = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	starts = [0, 2, 5]
	funcPy = getattr(kernels, 'awkward_IndexedArray_local_preparenext')
	funcPy(tocarry = tocarry,nextlen = nextlen,nextparents = nextparents,parentslength = parentslength,parents = parents,starts = starts)
	pytest_tocarry = [0, 1, 2, 3, -1, -1, 4, 5, 6, -1, -1]
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_local_preparenext_3():
	tocarry = []
	nextlen = 0
	nextparents = []
	parentslength = 0
	parents = []
	starts = []
	funcPy = getattr(kernels, 'awkward_IndexedArray_local_preparenext')
	funcPy(tocarry = tocarry,nextlen = nextlen,nextparents = nextparents,parentslength = parentslength,parents = parents,starts = starts)
	pytest_tocarry = []
	assert tocarry == pytest_tocarry


def test_awkward_IndexedArray_local_preparenext_4():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	nextlen = 9
	nextparents = [0, 0, 0, 2, 2, 3, 4, 4, 4]
	parentslength = 17
	parents = [0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
	starts = [0, 5, 8, 11, 14]
	funcPy = getattr(kernels, 'awkward_IndexedArray_local_preparenext')
	funcPy(tocarry = tocarry,nextlen = nextlen,nextparents = nextparents,parentslength = parentslength,parents = parents,starts = starts)
	pytest_tocarry = [0, 1, 2, -1, -1, -1, -1, -1, 3, 4, -1, 5, -1, -1, 6, 7, 8]
	assert tocarry == pytest_tocarry


