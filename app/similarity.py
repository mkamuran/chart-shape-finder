import math

import numpy as np


TARGET_POINTS = 80


def resample(values, length=TARGET_POINTS):
	if len(values) == 0:
		return []

	if len(values) == 1:
		return [float(values[0])] * length

	source_x = np.linspace(0, 1, len(values))
	target_x = np.linspace(0, 1, length)
	return np.interp(target_x, source_x, np.asarray(values, dtype=float)).tolist()


def normalize(values):
	clean = np.asarray(values, dtype=float)
	clean = clean[np.isfinite(clean)]

	if clean.size == 0:
		return []

	low = float(clean.min())
	high = float(clean.max())

	if math.isclose(low, high):
		return [0.5] * clean.size

	return ((clean - low) / (high - low)).tolist()


def prepare_series(values, length=TARGET_POINTS):
	return normalize(resample(values, length))


def similarity_score(draw_series, price_series):
	if len(draw_series) != len(price_series) or not draw_series:
		return 0

	diff = np.asarray(draw_series) - np.asarray(price_series)
	rmse = math.sqrt(float(np.mean(diff * diff)))
	return max(0, min(100, (1 - rmse) * 100))
