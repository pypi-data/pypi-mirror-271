import numpy
import logging


_logger = logging.getLogger(__name__)


def fast_vs_for_dipoles(
	dot_inputs: numpy.ndarray, dipoles: numpy.ndarray
) -> numpy.ndarray:
	"""
	No error correction here baby.
	Expects dot_inputs to be numpy array of [rx, ry, rz, f] entries, so a n by 4 where n is number of measurement points.
	"""
	# name indexes:
	# A: dipole config index
	# cart: cartesian index
	# m: measurement index

	# [A, cart]
	ps = dipoles[:, 0:3]
	ss = dipoles[:, 3:6]
	# [A]
	ws = dipoles[:, 6]

	_logger.debug(f"ps: {ps}")
	_logger.debug(f"ss: {ss}")
	_logger.debug(f"ws: {ws}")

	# [m, cart]
	rs = dot_inputs[:, 0:3]
	# [m]
	fs = dot_inputs[:, 3]

	# [m, cart] - [A, 1, cart]
	# [A, m, cart]
	diffses = rs - ss[:, None]

	_logger.debug(f"diffses: {diffses}")
	# [A, m]
	norms = numpy.linalg.norm(diffses, axis=2) ** 3
	_logger.debug(f"norms: {norms}")
	# [A, m, cart] [A, cart] -> [A, m]
	ases = (numpy.einsum("...ji, ...i", diffses, ps) / norms) ** 2
	_logger.debug(f"ases: {ases}")

	# [A, 1], denom [m] + [A, 1] -> [A, m]
	# [A, m]
	bses = 2 * ws[:, None] / ((numpy.pi * fs) ** 2 + ws[:, None] ** 2)

	_logger.debug(f"bses: {bses}")
	# returns shape [A, m]
	return ases * bses


def fast_vs_for_dipoleses(
	dot_inputs: numpy.ndarray, dipoleses: numpy.ndarray
) -> numpy.ndarray:
	"""
	No error correction here baby.
	Expects dot_inputs to be numpy array of [rx, ry, rz, f] entries, so a n by 4 where n is number of measurement points.

	Dipoleses are expected to be array of arrays of arrays: list of sets of dipoles which are part of a single arrangement to be added together.
	"""
	ps = dipoleses[:, :, 0:3]
	ss = dipoleses[:, :, 3:6]
	ws = dipoleses[:, :, 6]

	_logger.debug(f"ps: {ps}")
	_logger.debug(f"ss: {ss}")
	_logger.debug(f"ws: {ws}")

	rs = dot_inputs[:, 0:3]
	fs = dot_inputs[:, 3]

	diffses = rs[:, None] - ss[:, None, :]

	_logger.debug(f"diffses: {diffses}")
	norms = numpy.linalg.norm(diffses, axis=3) ** 3
	_logger.debug(f"norms: {norms}")
	ases = (numpy.einsum("abcd,acd->abc", diffses, ps) / norms) ** 2
	_logger.debug(f"ases: {ases}")

	bses = 2 * ws[:, None, :] / ((numpy.pi * fs[:, None]) ** 2 + ws[:, None, :] ** 2)
	_logger.debug(f"bses: {bses}")
	return numpy.einsum("...j->...", ases * bses)


def fast_efieldxs_for_dipoles(
	dot_inputs: numpy.ndarray, dipoles: numpy.ndarray
) -> numpy.ndarray:
	"""
	No error correction here baby.
	Expects dot_inputs to be numpy array of [rx, ry, rz, f] entries, so a n by 4 where n is number of measurement points.
	"""
	# name indexes:
	# A: dipole config index
	# j: dipole index within a config
	# cart: cartesian index
	# m: measurement index

	# Indexes [A, cart]
	ps = dipoles[:, 0:3]
	ss = dipoles[:, 3:6]
	# Indexes [A]
	ws = dipoles[:, 6]

	# Indexes [m, cart]
	rs = dot_inputs[:, 0:3]
	# Indexes [m]
	fs = dot_inputs[:, 3]

	# Indexes [m, cart] - [A, 1, cart]
	# Broadcasting from right
	# diffses.indexes [A, m, cart]
	diffses = rs - ss[:, None, :]

	# [A, m, cart][2] = cart
	# norms takes out axis 2, the last one, giving [A, m]
	norms = numpy.linalg.norm(diffses, axis=2)

	# long story but this ends up becoming (A, 1, j)
	# Some evidence is looking at ps term, which has shape (A, 1, j, cart=0) becoming (A, 1, j)

	# [A, m, cart] einsum [A, cart] explicitly gives [A, m]
	dot_products = numpy.einsum("amc,ac->am", diffses, ps) / (norms**2)

	# [m, A] * [cart, m, A] -> [cart, m, A], transpose that and you get [A, m, cart]
	projections = numpy.transpose(
		numpy.transpose(dot_products) * numpy.transpose(diffses)
	)

	# numerator [A, m, cart] - [A, 1, cart] -> [A, m, cart][:, :, 0] -> [A, m]
	alphas = (3 * projections - ps[:, numpy.newaxis])[:, :, 0] / norms**3

	# [A, m]
	ases = alphas**2

	# [A, 1], denom [m] + [A, 1] -> [A, m]
	# [A, m]
	bses = 2 * ws[:, None] / ((numpy.pi * fs) ** 2 + ws[:, None] ** 2)

	# return shape [A, m, j]
	return ases * bses


def fast_efieldxs_for_dipoleses(
	dot_inputs: numpy.ndarray, dipoleses: numpy.ndarray
) -> numpy.ndarray:
	"""
	No error correction here baby.
	Expects dot_inputs to be numpy array of [rx, ry, rz, f] entries, so a n by 4 where n is number of measurement points.

	Dipoleses are expected to be array of arrays of arrays:
	list of sets of dipoles which are part of a single arrangement to be added together.
	"""
	# name indexes:
	# A: dipole config index
	# j: dipole index within a config
	# cart: cartesian index
	# m: measurement index

	# Indexes [A, j, cart]
	ps = dipoleses[:, :, 0:3]
	ss = dipoleses[:, :, 3:6]
	# Indexes [A, j]
	ws = dipoleses[:, :, 6]

	# Indexes [m, cart]
	rs = dot_inputs[:, 0:3]
	# Indexes [m]
	fs = dot_inputs[:, 3]

	# Indexes [m, 1, cart] - [A, 1, j, cart]
	# Broadcasting from right
	# diffses.indexes [A, m, j, cart]
	diffses = rs[:, None] - ss[:, None, :]

	# norms takes out axis 3, the last one, giving [A, m, j]
	norms = numpy.linalg.norm(diffses, axis=3)

	# long story but this ends up becoming (A, 1, j)
	# Some evidence is looking at ps term, which has shape (A, 1, j, cart=0) becoming (A, 1, j)
	alphas = (
		(
			3
			* numpy.transpose(
				numpy.transpose(
					numpy.einsum("abcd,acd->abc", diffses, ps) / (norms**2)
				)
				* numpy.transpose(diffses)
			)[:, :, :, 0]
		)
		- ps[:, numpy.newaxis, :, 0]
	) / (norms**3)
	ases = alphas**2
	# bses.shape [A, m, j)]
	bses = 2 * ws[:, None, :] / ((numpy.pi * fs[:, None]) ** 2 + ws[:, None, :] ** 2)

	# return shape [A, m, j]
	return numpy.einsum("...j->...", ases * bses)


def fast_vs_for_asymmetric_dipoleses(
	dot_inputs: numpy.ndarray, dipoleses: numpy.ndarray, temp: numpy.ndarray
) -> numpy.ndarray:
	"""
	No error correction here baby.
	Expects dot_inputs to be numpy array of [rx, ry, rz, f] entries, so a n by 4 where n is number of measurement points.

	Dipoleses are expected to be array of arrays of arrays:
	list of sets of dipoles which are part of a single arrangement to be added together.
	Within each dipole, the expected format is [px, py, pz, sx, sy, sz, e1, e2, w]
	The passed in w is expected to be half the actual. This is bad, but here for historical reasons to be changed later.
	"""
	raw_ps = dipoleses[:, :, 0:3]
	ss = dipoleses[:, :, 3:6]
	e1s = dipoleses[:, :, 6]
	e2s = dipoleses[:, :, 7]
	raw_ws = dipoleses[:, :, 8]

	rs = dot_inputs[:, 0:3]
	fs = dot_inputs[:, 3]

	diffses = rs[:, None] - ss[:, None, :]

	_logger.warning(
		"This method is very likely to be broken, and should not be used without more thought"
	)
	w1s = numpy.exp(-e1s / temp) * raw_ws
	w2s = numpy.exp(-e2s / temp) * raw_ws

	mag_prefactor = 4 * ((w1s * w2s) / ((w1s + w2s) ** 2))
	ws = w1s + w2s

	# some annoying broadcast thing here?
	ps = (raw_ps.T * mag_prefactor.T).T

	norms = numpy.linalg.norm(diffses, axis=3) ** 3

	ases = (numpy.einsum("abcd,acd->abc", diffses, ps) / norms) ** 2

	bses = ws[:, None, :] / ((numpy.pi * fs[:, None]) ** 2 + ws[:, None, :] ** 2)

	return numpy.einsum("...j->...", ases * bses)


def between(a: numpy.ndarray, low: numpy.ndarray, high: numpy.ndarray) -> numpy.ndarray:
	"""
	Intended specifically for the case where a is a list of arrays, and each array must be between the single array low and high, but without error checking.
	"""
	return numpy.all(numpy.logical_and(low < a, high > a), axis=1)
