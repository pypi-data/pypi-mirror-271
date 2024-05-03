from dataclasses import dataclass
from typing import Sequence
import numpy
from pdme.subspace_simulation.mcmc_costs import (
	proportional_cost,
	proportional_costs_vs_actual_measurement,
)


@dataclass
class DipoleStandardDeviation:
	"""
	contains the dipole standard deviation to be used in porposals for markov chain monte carlo
	"""

	p_phi_step: float
	p_theta_step: float
	rx_step: float
	ry_step: float
	rz_step: float
	w_log_step: float


class MCMCStandardDeviation:
	"""
	wrapper for multiple standard deviations, allows for flexible length stuff
	"""

	def __init__(self, stdevs: Sequence[DipoleStandardDeviation]):
		self.stdevs = stdevs
		if len(stdevs) < 1:
			raise ValueError(f"Got stdevs: {stdevs}, must have length > 1")

	def __getitem__(self, key):
		newkey = key % len(self.stdevs)
		return self.stdevs[newkey]


def sort_array_of_dipoles_by_frequency(configuration) -> numpy.ndarray:
	"""
	Say we have a situation of 2 dipoles, and we've created 8 samples. Then we'll have an (8, 2, 7) numpy array.
	For each of the 8 samples, we want the 2 dipoles to be in order of frequency.

	Utility function.
	"""
	return numpy.array(sorted(configuration, key=lambda l: l[6]))


__all__ = [
	"DipoleStandardDeviation",
	"MCMCStandardDeviation",
	"sort_array_of_dipoles_by_frequency",
	"proportional_cost",
	"proportional_costs_vs_actual_measurement",
]
