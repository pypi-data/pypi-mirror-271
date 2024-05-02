from numpy import ndarray
from deepdog.direct_monte_carlo.direct_mc import DirectMonteCarloFilter
from typing import Sequence
import pdme.measurement
import pdme.measurement.input_types
import pdme.util.fast_nonlocal_spectrum
import pdme.util.fast_v_calc
import numpy


class SingleDotPotentialFilter(DirectMonteCarloFilter):
	def __init__(self, measurements: Sequence[pdme.measurement.DotRangeMeasurement]):
		self.measurements = measurements
		self.dot_inputs = [(measure.r, measure.f) for measure in self.measurements]

		self.dot_inputs_array = pdme.measurement.input_types.dot_inputs_to_array(
			self.dot_inputs
		)
		(
			self.lows,
			self.highs,
		) = pdme.measurement.input_types.dot_range_measurements_low_high_arrays(
			self.measurements
		)

	def filter_samples(self, samples: ndarray) -> ndarray:
		current_sample = samples
		for di, low, high in zip(self.dot_inputs_array, self.lows, self.highs):

			if len(current_sample) < 1:
				break
			vals = pdme.util.fast_v_calc.fast_vs_for_dipoleses(
				numpy.array([di]), current_sample
			)

			current_sample = current_sample[
				numpy.all((vals > low) & (vals < high), axis=1)
			]
		return current_sample


class SingleDotSpinQubitFrequencyFilter(DirectMonteCarloFilter):
	def __init__(self, measurements: Sequence[pdme.measurement.DotRangeMeasurement]):
		self.measurements = measurements
		self.dot_inputs = [(measure.r, measure.f) for measure in self.measurements]

		self.dot_inputs_array = pdme.measurement.input_types.dot_inputs_to_array(
			self.dot_inputs
		)
		(
			self.lows,
			self.highs,
		) = pdme.measurement.input_types.dot_range_measurements_low_high_arrays(
			self.measurements
		)

	# oh no not this again
	def fast_s_spin_qubit_tarucha_apsd_dipoleses(
		self, dot_inputs: numpy.ndarray, dipoleses: numpy.ndarray
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

		# dot_index is either 0 or 1 for dot1 or dot2
		# hopefully this adhoc grammar is making sense, with the explicit labelling of the values of the last axis in cartesian space
		# axes are [measurement_idx, {dot_index}, {rx, ry, rz}] where the inner {dot_index} is gone
		# [measurement_idx, cartesian3]
		rs = dot_inputs[:, 0:3]
		# axes are [measurement_idx]
		fs = dot_inputs[:, 3]

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
		diffses = rs[:, None] - ss[:, None, :]

		# norms takes out axis 3, the last one, giving [A, measurement_idx, j]
		norms = numpy.linalg.norm(diffses, axis=3)

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
		alphses = (
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

		bses = (
			2
			* numpy.pi
			* ws[:, None, :]
			/ ((2 * numpy.pi * fs[:, None]) ** 2 + 4 * ws[:, None, :] ** 2)
		)

		return numpy.einsum("...j->...", alphses * alphses * bses)

	def filter_samples(self, samples: ndarray) -> ndarray:
		current_sample = samples
		for di, low, high in zip(self.dot_inputs_array, self.lows, self.highs):

			if len(current_sample) < 1:
				break
			vals = self.fast_s_spin_qubit_tarucha_apsd_dipoleses(
				numpy.array([di]), current_sample
			)
			# _logger.info(vals)

			current_sample = current_sample[
				numpy.all((vals > low) & (vals < high), axis=1)
			]
		# _logger.info(f"leaving with {len(current_sample)}")
		return current_sample


class DoubleDotSpinQubitFrequencyFilter(DirectMonteCarloFilter):
	def __init__(
		self,
		pair_phase_measurements: Sequence[pdme.measurement.DotPairRangeMeasurement],
	):
		self.pair_phase_measurements = pair_phase_measurements
		self.dot_pair_inputs = [
			(measure.r1, measure.r2, measure.f)
			for measure in self.pair_phase_measurements
		]
		self.dot_pair_inputs_array = (
			pdme.measurement.input_types.dot_pair_inputs_to_array(self.dot_pair_inputs)
		)
		(
			self.pair_phase_lows,
			self.pair_phase_highs,
		) = pdme.measurement.input_types.dot_range_measurements_low_high_arrays(
			self.pair_phase_measurements
		)

	def filter_samples(self, samples: ndarray) -> ndarray:
		current_sample = samples

		for pi, plow, phigh in zip(
			self.dot_pair_inputs_array, self.pair_phase_lows, self.pair_phase_highs
		):
			if len(current_sample) < 1:
				break

			vals = pdme.util.fast_nonlocal_spectrum.signarg(
				pdme.util.fast_nonlocal_spectrum.fast_s_spin_qubit_tarucha_nonlocal_dipoleses(
					numpy.array([pi]), current_sample
				)
			)
			current_sample = current_sample[
				numpy.all(
					((vals > plow) & (vals < phigh)) | ((vals < plow) & (vals > phigh)),
					axis=1,
				)
			]
		return current_sample
