import numpy
import numpy.random
from pdme.model.model import DipoleModel
from pdme.measurement import (
	OscillatingDipole,
	OscillatingDipoleArrangement,
)
import pdme.subspace_simulation
from typing import Optional


class LogSpacedRandomCountMultipleDipoleFixedMagnitudeXYModel(DipoleModel):
	"""
	Model of multiple oscillating dipoles with a fixed magnitude, but free rotation in XY plane. Spaced logarithmically.

	Parameters
	----------

	wexp_min: log-10 lower bound for dipole frequency
	wexp_min: log-10 upper bound for dipole frequency

	pfixed : float
	The fixed dipole magnitude.

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
		self.rng = numpy.random.default_rng()
		self.n_max = n_max
		if prob_occupancy >= 1 or prob_occupancy <= 0:
			raise ValueError(
				f"The probability of a dipole site occupancy must be between 0 and 1, got {prob_occupancy}"
			)
		self.prob_occupancy = prob_occupancy

	def __repr__(self) -> str:
		return f"LogSpacedRandomCountMultipleDipoleFixedMagnitudeXYModel({self.xmin}, {self.xmax}, {self.ymin}, {self.ymax}, {self.zmin}, {self.zmax}, {self.wexp_min}, {self.wexp_max}, {self.pfixed}, {self.n_max}, {self.prob_occupancy})"

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
			phi = rng.uniform(0, 2 * numpy.pi)
			px = self.pfixed * numpy.cos(phi)
			py = self.pfixed * numpy.sin(phi)
			pz = 0
			s_pts = numpy.array(
				(
					rng.uniform(self.xmin, self.xmax),
					rng.uniform(self.ymin, self.ymax),
					rng.uniform(self.zmin, self.zmax),
				)
			)
			frequency = 10 ** rng.uniform(self.wexp_min, self.wexp_max)

			dipoles.append(
				OscillatingDipole(numpy.array([px, py, pz]), s_pts, frequency)
			)
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
		phi = 2 * numpy.pi * rng.random(shape)

		p_mask = rng.binomial(1, self.prob_occupancy, shape)
		p_magnitude = self.pfixed * p_mask

		px = p_magnitude * numpy.cos(phi)
		py = p_magnitude * numpy.sin(phi)
		pz = p_magnitude * 0

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
		phi = numpy.arctan2(py, px)

		# need to step phi, rx, ry, rz, w
		# then p^\ast is 1/(2 phi_step) and Delta = phi_step(2 * {0, 1} - 1)
		delta_phi = stdev.p_phi_step * rng_to_use.uniform(-1, 1)
		tentative_phi = phi + delta_phi

		tentative_px = self.pfixed * numpy.cos(tentative_phi)
		tentative_py = self.pfixed * numpy.sin(tentative_phi)

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
				tentative_px,
				tentative_py,
				pz,
				tentative_rx,
				tentative_ry,
				tentative_rz,
				tentative_w,
			]
		)
		return tentative_dip
