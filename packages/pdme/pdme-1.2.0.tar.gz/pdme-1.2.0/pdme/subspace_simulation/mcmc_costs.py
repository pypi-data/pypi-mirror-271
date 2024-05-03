import numpy
import numpy.typing
import pdme.util.fast_v_calc


def proportional_cost(a: numpy.ndarray, b: numpy.ndarray) -> numpy.ndarray:
	tops = numpy.max(b / a, axis=-1)
	bottoms = numpy.max(a / b, axis=-1)
	return numpy.maximum(tops, bottoms)


def proportional_costs_vs_actual_measurement(
	dot_inputs_array: numpy.ndarray,
	actual_measurement_array: numpy.ndarray,
	dipoles_to_test: numpy.ndarray,
) -> numpy.ndarray:
	vals = pdme.util.fast_v_calc.fast_vs_for_dipoleses(
		dot_inputs_array, dipoles_to_test
	)
	return proportional_cost(actual_measurement_array, vals)
