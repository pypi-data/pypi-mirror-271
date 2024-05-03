import numpy
import numpy.random
from pdme.measurement import (
	OscillatingDipoleArrangement,
)
import logging
import pdme.subspace_simulation
from typing import List, Tuple, Optional

_logger = logging.getLogger(__name__)


class DipoleModel:
	"""
	Interface for models based on dipoles.
	Some concepts are kept specific for dipole-based models, even though other types of models could be useful later on.
	"""

	def get_dipoles(
		self, max_frequency: float, rng: numpy.random.Generator = None
	) -> OscillatingDipoleArrangement:
		"""
		For a particular maximum frequency, gets a dipole arrangement based on the model that uniformly distributes its choices according to the model.
		If no rng is passed in, uses some default, but you might not want that.
		Frequencies should be chosen uniformly on range of (0, max_frequency).
		"""
		raise NotImplementedError

	def get_monte_carlo_dipole_inputs(
		self, n: int, max_frequency: float, rng: numpy.random.Generator = None
	) -> numpy.ndarray:
		"""
		For a given DipoleModel, gets a set of dipole collections as a monte_carlo_n x dipole_count x 7 numpy array.
		"""
		raise NotImplementedError

	def markov_chain_monte_carlo_proposal(
		self,
		dipole: numpy.ndarray,
		stdev: pdme.subspace_simulation.DipoleStandardDeviation,
		rng_arg: Optional[numpy.random.Generator] = None,
	) -> numpy.ndarray:
		raise NotImplementedError

	def get_mcmc_chain(
		self,
		seed,
		cost_function,
		chain_length,
		threshold_cost: float,
		stdevs: pdme.subspace_simulation.MCMCStandardDeviation,
		initial_cost: Optional[float] = None,
		rng_arg: Optional[numpy.random.Generator] = None,
	) -> List[Tuple[float, numpy.ndarray]]:
		"""
		performs constrained markov chain monte carlo starting on seed parameter.
		The cost function given is used as a constrained to condition the chain;
		a new state is only accepted if cost_function(state) < cost_function(previous_state).
		The stdevs passed in are the stdevs we're expected to use.

		Because we're using this for subspace simulation where our proposal function is not too important, we're in good shape.
		Note that for our adaptive stdevs to work, there's an unwritten contract that we sort each dipole in the state by frequency (increasing).

		The seed is a list of dipoles, and each chain state is a list of dipoles as well.

		initial_cost is a performance guy that lets you pre-populate the initial cost used to define the condition.
		Probably premature optimisation.

		Returns a chain of [ (cost: float, state: dipole_ndarray ) ] format.
		"""
		_logger.debug(
			f"Starting Markov Chain Monte Carlo with seed: {seed} for chain length {chain_length} and provided stdevs {stdevs}"
		)
		chain: List[Tuple[float, numpy.ndarray]] = []
		if initial_cost is None:
			current_cost = cost_function(numpy.array([seed]))
		else:
			current_cost = initial_cost
		current = seed
		for i in range(chain_length):
			dips = []
			for dipole_index, dipole in enumerate(current):
				_logger.debug(dipole_index)
				_logger.debug(dipole)
				stdev = stdevs[dipole_index]
				tentative_dip = self.markov_chain_monte_carlo_proposal(
					dipole, stdev, rng_arg
				)

				dips.append(tentative_dip)
			dips_array = pdme.subspace_simulation.sort_array_of_dipoles_by_frequency(
				dips
			)
			tentative_cost = cost_function(numpy.array([dips_array]))[0]
			if tentative_cost < threshold_cost:
				chain.append((numpy.squeeze(tentative_cost).item(), dips_array))
				current = dips_array
				current_cost = tentative_cost
			else:
				chain.append((numpy.squeeze(current_cost).item(), current))
		return chain
