import numpy
import logging


_logger = logging.getLogger(__name__)


def fast_s_nonlocal(
	dot_pair_inputs: numpy.ndarray, dipoles: numpy.ndarray
) -> numpy.ndarray:
	"""
	No error correction here baby.
	"""
	ps = dipoles[:, 0:3]
	ss = dipoles[:, 3:6]
	ws = dipoles[:, 6]

	_logger.debug(f"ps: {ps}")
	_logger.debug(f"ss: {ss}")
	_logger.debug(f"ws: {ws}")

	r1s = dot_pair_inputs[:, 0, 0:3]
	r2s = dot_pair_inputs[:, 1, 0:3]
	f1s = dot_pair_inputs[:, 0, 3]
	f2s = dot_pair_inputs[:, 1, 3]

	if (f1s != f2s).all():
		raise ValueError(f"Dot pair frequencies are inconsistent: {dot_pair_inputs}")

	diffses1 = r1s - ss[:, None]
	diffses2 = r2s - ss[:, None]
	if _logger.isEnabledFor(logging.DEBUG):
		_logger.debug(f"diffses1: {diffses1}")
		_logger.debug(f"diffses2: {diffses2}")

	norms1 = numpy.linalg.norm(diffses1, axis=2) ** 3
	norms2 = numpy.linalg.norm(diffses2, axis=2) ** 3
	if _logger.isEnabledFor(logging.DEBUG):
		_logger.debug(f"norms1: {norms1}")
		_logger.debug(f"norms2: {norms2}")

	alphses1 = numpy.einsum("...ji, ...i", diffses1, ps) / norms1
	alphses2 = numpy.einsum("...ji, ...i", diffses2, ps) / norms2
	if _logger.isEnabledFor(logging.DEBUG):
		_logger.debug(f"alphses1: {alphses1}")
		_logger.debug(f"alphses2: {alphses2}")

	bses = 2 * ws[:, None] / ((numpy.pi * f1s) ** 2 + ws[:, None] ** 2)
	if _logger.isEnabledFor(logging.DEBUG):
		_logger.debug(f"bses: {bses}")

	return alphses1 * alphses2 * bses


def fast_s_nonlocal_dipoleses(
	dot_pair_inputs: numpy.ndarray, dipoleses: numpy.ndarray
) -> numpy.ndarray:
	"""
	No error correction here baby.
	"""

	# We're going to annotate the indices on this class.
	# Let's define some indices:
	# A -> index of dipoleses configurations
	# measurement_index -> if we have 100 frequencies for example, indexes which one of them it is
	# j -> within a particular configuration, indexes dipole j
	# If we need to use numbers, let's use A -> 2, j -> 10, measurement_index -> 9 for consistency with
	# my other notes
	# cart -> {x, y, z} is a cartesian axis

	# ps, ss have shape [A, j, cart]
	ps = dipoleses[:, :, 0:3]
	ss = dipoleses[:, :, 3:6]
	# ws shape [A, j]
	ws = dipoleses[:, :, 6]

	_logger.debug(f"ps: {ps}")
	_logger.debug(f"ss: {ss}")
	_logger.debug(f"ws: {ws}")

	# rs have shape [meas_idx, {}, cart], where the inner index goes away leaving
	# [meas, cart]
	r1s = dot_pair_inputs[:, 0, 0:3]
	r2s = dot_pair_inputs[:, 1, 0:3]
	# fs have index [meas_idx], this makes sense
	f1s = dot_pair_inputs[:, 0, 3]
	f2s = dot_pair_inputs[:, 1, 3]

	if (f1s != f2s).all():
		raise ValueError(f"Dot pair frequencies are inconsistent: {dot_pair_inputs}")

	# r1s have shape [meas, cart], adding the none makes it
	# r1s[:, None].shape = [meas, 1, cart]
	# ss[:, None, :].shape = [A, 1, j, cart]
	# subtracting broadcasts by matching from the right to the left, giving a final shape of
	# diffses.shape [A, meas, j, cart]
	diffses1 = r1s[:, None] - ss[:, None, :]
	diffses2 = r2s[:, None] - ss[:, None, :]
	if _logger.isEnabledFor(logging.DEBUG):
		_logger.debug(f"diffses1: {diffses1}")
		_logger.debug(f"diffses2: {diffses2}")

	# norming on the cartesian axis, which is axis 3 as seen above
	# norms.shape [A, meas, j]
	norms1 = numpy.linalg.norm(diffses1, axis=3) ** 3
	norms2 = numpy.linalg.norm(diffses2, axis=3) ** 3
	if _logger.isEnabledFor(logging.DEBUG):
		_logger.debug(f"norms1: {norms1}")
		_logger.debug(f"norms2: {norms2}")

	# diffses shape [A, meas, j, cart]
	# ps shape [A, j, cart]
	# so we're summing over the d axis, the cartesian one.
	# final shape of numerator is [A, meas, j]
	# denom shape is [A, meas, j]
	# final shape stayes [A, meas, j]
	alphses1 = numpy.einsum("abcd,acd->abc", diffses1, ps) / norms1
	alphses2 = numpy.einsum("abcd,acd->abc", diffses2, ps) / norms2
	if _logger.isEnabledFor(logging.DEBUG):
		_logger.debug(f"alphses1: {alphses1}")
		_logger.debug(f"alphses2: {alphses2}")

	# ws shape [A, j], so numerator has shape [A, 1, j]
	# f1s shape is [meas], so first term of denom is [meas, 1]
	# ws[:, None, :].shape [A, 1, j] so breadcasting the sum in denom gives
	# denom.shape [A meas, j]
	# so now overall shape is [A, meas, j]
	bses = 2 * ws[:, None, :] / ((numpy.pi * f1s[:, None]) ** 2 + ws[:, None, :] ** 2)
	if _logger.isEnabledFor(logging.DEBUG):
		_logger.debug(f"bses: {bses}")

	# so our output shape is [A, meas, j]
	_logger.debug(f"Raw pair calc: [{alphses1 * alphses2 * bses}]")
	return numpy.einsum("...j->...", alphses1 * alphses2 * bses)


def fast_s_spin_qubit_tarucha_nonlocal_dipoleses(
	dot_pair_inputs: numpy.ndarray, dipoleses: numpy.ndarray
) -> numpy.ndarray:
	"""
	No error correction here baby.
	"""

	# We're going to annotate the indices on this class.
	# Let's define some indices:
	# A -> index of dipoleses configurations
	# j -> within a particular configuration, indexes dipole j
	# measurement_index -> if we have 100 frequencies for example, indexes which one of them it is
	# If we need to use numbers, let's use A -> 2, j -> 10, measurement_index -> 9 for consistency with
	# my other notes

	# axes are [dipole_config_idx A, dipole_idx j, {px, py, pz}3]
	ps = dipoleses[:, :, 0:3]
	# axes are [dipole_config_idx A, dipole_idx j, {sx, sy, sz}3]
	ss = dipoleses[:, :, 3:6]
	# axes are [dipole_config_idx A, dipole_idx j, w], last axis is just 1
	ws = dipoleses[:, :, 6]

	_logger.debug(f"ps: {ps}")
	_logger.debug(f"ss: {ss}")
	_logger.debug(f"ws: {ws}")

	# dot_index is either 0 or 1 for dot1 or dot2
	# hopefully this adhoc grammar is making sense, with the explicit labelling of the values of the last axis in cartesian space
	# axes are [measurement_idx, {dot_index}, {rx, ry, rz}] where the inner {dot_index} is gone
	# [measurement_idx, cartesian3]
	r1s = dot_pair_inputs[:, 0, 0:3]
	r2s = dot_pair_inputs[:, 1, 0:3]
	# axes are [measurement_idx]
	f1s = dot_pair_inputs[:, 0, 3]
	f2s = dot_pair_inputs[:, 1, 3]

	if (f1s != f2s).all():
		raise ValueError(f"Dot pair frequencies are inconsistent: {dot_pair_inputs}")

	# first operation!
	# r1s has shape [measurement_idx, rxs]
	# None inserts an extra axis so the r1s[:, None] has shape
	# [measurement_idx, 1]([rxs]) with the last rxs hidden
	#
	# ss has shape [ A, j, {sx, sy, sz}3], so second term has shape [A, 1, j]([sxs])
	# these broadcast from right to left
	# [	 measurement_idx, 1, rxs]
	# [A,	  1,			   j, sxs]
	# resulting in [A, measurement_idx, j, cart3] sxs rxs are both cart3
	diffses1 = r1s[:, None] - ss[:, None, :]
	diffses2 = r2s[:, None] - ss[:, None, :]
	if _logger.isEnabledFor(logging.DEBUG):
		_logger.debug(f"diffses1: {diffses1}")
		_logger.debug(f"diffses2: {diffses2}")

	# norms takes out axis 3, the last one, giving [A, measurement_idx, j]
	norms1 = numpy.linalg.norm(diffses1, axis=3)
	norms2 = numpy.linalg.norm(diffses2, axis=3)
	if _logger.isEnabledFor(logging.DEBUG):
		_logger.debug(f"norms1: {norms1}")
		_logger.debug(f"norms2: {norms2}")

	# _logger.info(f"norms1: {norms1}")
	# _logger.info(f"norms1 shape: {norms1.shape}")
	#
	# diffses1 (A, measurement_idx, j, xs)
	# ps:  (A, j, px)
	# result is (A, measurement_idx, j)
	# intermediate_dot_prod = numpy.einsum("abcd,acd->abc", diffses1, ps)
	# _logger.info(f"dot product shape: {intermediate_dot_prod.shape}")

	# transpose makes it (j, measurement_idx, A)
	# transp_intermediate_dot_prod = numpy.transpose(numpy.einsum("abcd,acd->abc", diffses1, ps) / (norms1**3))

	# transpose of diffses has shape (xs, j, measurement_idx, A)
	# numpy.transpose(diffses1)
	# _logger.info(f"dot product shape: {transp_intermediate_dot_prod.shape}")

	# inner transpose is (j, measurement_idx, A) * (xs, j, measurement_idx, A)
	# next transpose puts it back to (A, measurement_idx, j, xs)
	# p_dot_r_times_r_term = 3 * numpy.transpose(numpy.transpose(numpy.einsum("abcd,acd->abc", diffses1, ps) / (norms1**3)) * numpy.transpose(diffses1))
	# _logger.info(f"p_dot_r_times_r_term: {p_dot_r_times_r_term.shape}")

	# only x axis puts us at (A, measurement_idx, j)
	# p_dot_r_times_r_term_x_only = p_dot_r_times_r_term[:, :, :, 0]
	# _logger.info(f"p_dot_r_times_r_term_x_only.shape: {p_dot_r_times_r_term_x_only.shape}")

	# now to complete the numerator we subtract the ps, which are (A, j, px):
	# slicing off the end gives us (A, j), so we newaxis to get (A, 1, j)
	# _logger.info(ps[:, numpy.newaxis, :, 0].shape)
	alphses1 = (
		(
			3
			* numpy.transpose(
				numpy.transpose(
					numpy.einsum("abcd,acd->abc", diffses1, ps) / (norms1**2)
				)
				* numpy.transpose(diffses1)
			)[:, :, :, 0]
		)
		- ps[:, numpy.newaxis, :, 0]
	) / (norms1**3)
	alphses2 = (
		(
			3
			* numpy.transpose(
				numpy.transpose(
					numpy.einsum("abcd,acd->abc", diffses2, ps) / (norms2**2)
				)
				* numpy.transpose(diffses2)
			)[:, :, :, 0]
		)
		- ps[:, numpy.newaxis, :, 0]
	) / (norms2**3)
	if _logger.isEnabledFor(logging.DEBUG):
		_logger.debug(f"alphses1: {alphses1}")
		_logger.debug(f"alphses2: {alphses2}")

	bses = 2 * ws[:, None, :] / ((numpy.pi * f1s[:, None]) ** 2 + ws[:, None, :] ** 2)
	if _logger.isEnabledFor(logging.DEBUG):
		_logger.debug(f"bses: {bses}")

	_logger.debug(f"Raw pair calc: [{alphses1 * alphses2 * bses}]")
	return numpy.einsum("...j->...", alphses1 * alphses2 * bses)


def signarg(x, **kwargs):
	"""
	uses numpy.sign to implement Arg for real numbers only. Should return pi for negative inputs, 0 for positive.
	Passes through args to numpy.sign
	"""
	return numpy.pi * (numpy.sign(x, **kwargs) - 1) / (-2)
