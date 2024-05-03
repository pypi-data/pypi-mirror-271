import numpy
import numpy.random
from pdme.model.model import DipoleModel
from pdme.measurement import (
	OscillatingDipole,
	OscillatingDipoleArrangement,
)
import logging
from typing import Optional
import pdme.subspace_simulation

_logger = logging.getLogger(__name__)


class LogSpacedRandomCountMultipleDipoleFixedMagnitudeFixedOrientationModel(
	DipoleModel
):
	"""
	Model of multiple oscillating dipoles with a fixed magnitude and fixed rotation. Spaced log uniformly in relaxation time.

	Parameters
	----------

	wexp_min: log-10 lower bound for dipole frequency
	wexp_min: log-10 upper bound for dipole frequency

	pfixed : float
	The fixed dipole magnitude.

	thetafixed: float
	The fixed theta (polar angle).
	Should be between 0 and pi.

	phifixed: float
	The fixed phi (azimuthal angle).
	Should be between 0 and 2 pi.

	n_max : int
	The maximum number of dipoles.

	prob_occupancy : float
	The probability of dipole occupancy
	"""

	def __init__(
		self,
		xmin: float,
		xmax: float,
		ymin: float,
		ymax: float,
		zmin: float,
		zmax: float,
		wexp_min: float,
		wexp_max: float,
		pfixed: float,
		thetafixed: float,
		phifixed: float,
		n_max: int,
		prob_occupancy: float,
	) -> None:
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax
		self.zmin = zmin
		self.zmax = zmax
		self.wexp_min = wexp_min
		self.wexp_max = wexp_max
		self.pfixed = pfixed
		self.thetafixed = thetafixed
		self.phifixed = phifixed
		self.rng = numpy.random.default_rng()
		self.n_max = n_max

		px = self.pfixed * numpy.sin(self.thetafixed) * numpy.cos(self.phifixed)
		py = self.pfixed * numpy.sin(self.thetafixed) * numpy.sin(self.phifixed)
		pz = self.pfixed * numpy.cos(self.thetafixed)

		self.moment_fixed = numpy.array([px, py, pz])
		if prob_occupancy >= 1 or prob_occupancy <= 0:
			raise ValueError(
				f"The probability of a dipole site occupancy must be between 0 and 1, got {prob_occupancy}"
			)
		self.prob_occupancy = prob_occupancy

	def __repr__(self) -> str:
		return f"LogSpacedRandomCountMultipleDipoleFixedMagnitudeFixedOrientationModel({self.xmin}, {self.xmax}, {self.ymin}, {self.ymax}, {self.zmin}, {self.zmax}, {self.wexp_min}, {self.wexp_max}, {self.pfixed}, {self.thetafixed}, {self.phifixed}, {self.n_max}, {self.prob_occupancy})"

	def get_dipoles(
		self, max_frequency: float, rng_to_use: numpy.random.Generator = None
	) -> OscillatingDipoleArrangement:
		rng: numpy.random.Generator
		if rng_to_use is None:
			rng = self.rng
		else:
			rng = rng_to_use

		dipoles = []

		n = rng.binomial(self.n_max, self.prob_occupancy)

		for i in range(n):
			s_pts = numpy.array(
				(
					rng.uniform(self.xmin, self.xmax),
					rng.uniform(self.ymin, self.ymax),
					rng.uniform(self.zmin, self.zmax),
				)
			)
			frequency = 10 ** rng.uniform(self.wexp_min, self.wexp_max)

			dipoles.append(OscillatingDipole(self.moment_fixed, s_pts, frequency))
		return OscillatingDipoleArrangement(dipoles)

	def get_monte_carlo_dipole_inputs(
		self,
		monte_carlo_n: int,
		_: float,
		rng_to_use: numpy.random.Generator = None,
	) -> numpy.ndarray:

		rng: numpy.random.Generator
		if rng_to_use is None:
			rng = self.rng
		else:
			rng = rng_to_use

		shape = (monte_carlo_n, self.n_max)

		p_mask = rng.binomial(1, self.prob_occupancy, shape)

		# dipoles = numpy.einsum("ij,k->ijk", p_mask, self.moment_fixed)
		# Is there a better way to create the final array? probably! can create a flatter guy then reshape.
		# this is easier to reason about.
		p_magnitude = self.pfixed * p_mask

		px = p_magnitude * numpy.sin(self.thetafixed) * numpy.cos(self.phifixed)
		py = p_magnitude * numpy.sin(self.thetafixed) * numpy.sin(self.phifixed)
		pz = p_magnitude * numpy.cos(self.thetafixed)

		sx = rng.uniform(self.xmin, self.xmax, shape)
		sy = rng.uniform(self.ymin, self.ymax, shape)
		sz = rng.uniform(self.zmin, self.zmax, shape)

		w = 10 ** rng.uniform(self.wexp_min, self.wexp_max, shape)

		return numpy.stack([px, py, pz, sx, sy, sz, w], axis=-1)

	def markov_chain_monte_carlo_proposal(
		self,
		dipole: numpy.ndarray,
		stdev: pdme.subspace_simulation.DipoleStandardDeviation,
		rng_arg: Optional[numpy.random.Generator] = None,
	) -> numpy.ndarray:
		if rng_arg is None:
			rng_to_use = self.rng
		else:
			rng_to_use = rng_arg

		px = dipole[0]
		py = dipole[1]
		pz = dipole[2]
		# won't change p for this model of fixed dipole moment.

		rx = dipole[3]
		ry = dipole[4]
		rz = dipole[5]

		tentative_rx = rx + stdev.rx_step * rng_to_use.uniform(-1, 1)
		if tentative_rx < self.xmin or tentative_rx > self.xmax:
			tentative_rx = rx

		tentative_ry = ry + stdev.ry_step * rng_to_use.uniform(-1, 1)
		if tentative_ry < self.ymin or tentative_ry > self.ymax:
			tentative_ry = ry
		tentative_rz = rz + stdev.rz_step * rng_to_use.uniform(-1, 1)
		if tentative_rz < self.zmin or tentative_rz > self.zmax:
			tentative_rz = rz

		w = dipole[6]
		tentative_w = numpy.exp(
			numpy.log(w) + (stdev.w_log_step * rng_to_use.uniform(-1, 1))
		)
		tentative_dip = numpy.array(
			[
				px,
				py,
				pz,
				tentative_rx,
				tentative_ry,
				tentative_rz,
				tentative_w,
			]
		)
		return tentative_dip
