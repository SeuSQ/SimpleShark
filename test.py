import numpy
import pandas

a = numpy.array([12, 2])
b = pandas.Series(a)
print(isinstance(a, numpy.ndarray))
print(isinstance(b, pandas.Series))