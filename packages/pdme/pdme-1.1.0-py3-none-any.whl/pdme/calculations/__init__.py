"""
This module is a canonical source of the accurate expressions we want to use for calculating our noise.
No reference to class or anything, just a straight set of math functions.
"""
import numpy


def telegraph_beta(f: float, w: float) -> float:
	"""
	This function represents the frequency component of analytic telegraph noise.

	We're assuming we care about the one-sided PSD where we are ignoring negative frequencies.
	This matches with experimental data from say Connors et al., and I think is better than keeping with one-sided.
	Note that this means that it will only be comparable then with time series data assuming one-sided!

	Don't bikeshed yet, if we care about two-sided things for any reason down the line divide this by two or just change it then.
	"""
	return 2 * w / ((numpy.pi * f) ** 2 + w**2)


def electric_potential(p: numpy.ndarray, s: numpy.ndarray, r: numpy.ndarray) -> float:
	"""
	Gives the electric potential of a defect with dipole moment p, located at position s,
	as measured from position r.

	p, s, r, are numpy arrays of length 3
	"""
	diff = r - s
	return (p.dot(diff) / (numpy.linalg.norm(diff) ** 3)).item()


def electric_field(
	p: numpy.ndarray, s: numpy.ndarray, r: numpy.ndarray
) -> numpy.ndarray:
	"""
	Gives the electric field of a defect with dipole moment p, located at position s,
	as measured from position r.

	p, s, r, are numpy arrays of length 3

	Returns an array of length 3, ideally.
	"""
	diff = r - s
	norm_diff = numpy.linalg.norm(diff)

	return ((3 * (p.dot(diff) * diff) / (norm_diff**2)) - p) / (norm_diff**3)
