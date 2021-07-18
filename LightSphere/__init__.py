from LightStrip import LightStrip
from . import config as cfg
import math

FULL_CIRCLE = 360
HALF_CIRCLE = 180

class LightSphere:

	def __init__(self, strip = None):

		if not strip:
			strip = LightStrip()

		self._strip = strip
		self._zeroThetas = cfg.THETA_ZERO
		self._thetas = self._calculateThetas()
		self._phis   = self._calculatePhis()

	def _calculateThetas(self):

		# Pre-make theta array
		result = [None for i in range(len(self._strip))]

		for i in range(len(self._zeroThetas) - 1):

			lo = self._zeroThetas[i]
			hi = self._zeroThetas[i+ 1]
			ringSize = hi - lo
			deltaTheta = FULL_CIRCLE / ringSize

			for j in range(lo, hi):
				arc = (j - lo) * deltaTheta
				result[j] = arc

		result =  [(i, result[i]) for i in range(len(result))] 
		result += [(i, result[i][1] + FULL_CIRCLE) for i in range(len(result))]
		result += [(i, 2 * FULL_CIRCLE) for i in self._zeroThetas]

		result.sort(key=lambda x: x[1])

		return [
			[item[0] for item in result],
			[item[1] for item in result]
		]


	def _calculatePhis(self):

		deltaPhi = HALF_CIRCLE / (len(self._strip))
		result =  [(i, i * deltaPhi) for i in range(len(self._strip))] 
		result += [(i, result[i][1] + HALF_CIRCLE) for i in range(len(result))]

		result.sort(key=lambda x: x[1])

		return (
			[item[0] for item in result],
			[item[1] for item in result]
		)
		
	def _findBoundary(self, target, array):

		for i in range(len(array) - 1):
			lo = i
			hi = i + 1
			if array[lo] <= target and array[hi] >= target:
				result = (lo, hi)
				return result

		raise Exception(f"Boundary {target} was not found.")


	def fill(self, color, thetaRange=None, phiRange = None):

		# Set fill range to all if none is provided.
		if thetaRange is None:
			thetaRange = (0, FULL_CIRCLE)

		if phiRange is None:
			phiRange = (0, HALF_CIRCLE)

		# Adjust ranges to fit within the full- and half-circle ranges
		thetaRange = (
			thetaRange[0] - FULL_CIRCLE * math.floor(thetaRange[0] / FULL_CIRCLE),
			thetaRange[1] - FULL_CIRCLE * math.floor(thetaRange[1] / FULL_CIRCLE)
		)

		phiRange = (
			phiRange[0] - HALF_CIRCLE * math.floor(phiRange[0] / HALF_CIRCLE),
			phiRange[1] - HALF_CIRCLE * math.floor(phiRange[1] / HALF_CIRCLE)
		)

		# Add a half or full circle to make the max larger than the min
		if thetaRange[1] <= thetaRange[0]:
			thetaRange = (thetaRange[0], thetaRange[1] + FULL_CIRCLE)

		if phiRange[1] <= phiRange[0]:
			phiRange = (phiRange[0], phiRange[1] + HALF_CIRCLE)

		# Get all pixel angle indices and values from precomputed coordinate tables
		thetaIndices, thetaValues = self._thetas
		phiIndices, phiValues = self._phis

		# Find the index boundaries
		thetaRange = (
			self._findBoundary(thetaRange[0], thetaValues),
			self._findBoundary(thetaRange[1], thetaValues)
		)
		thetaRange = thetaIndices[thetaRange[0][1]:thetaRange[1][0]]

		phiRange = (
			self._findBoundary(phiRange[0], phiValues),
			self._findBoundary(phiRange[1], phiValues)
		)
		phiRange = phiIndices[phiRange[0][1]:phiRange[1][0]]

		# Set all pixels in both the theta and phi ranges to the color
		intsecRange = self._intersectLists(phiRange, thetaRange)
		self._strip[intsecRange] = color


	def clear(self):
		self._strip.clear()

	def show(self):
		self._strip.show()

	def setBrightness(self, brightness):
		self._strip.setBrightness(brightness)

	def _intersectLists(self, list1, list2):
		return [value for value in list1 if value in list2]

	def __setitem__ (self, key, color):
		"""
		Sets the value at an index or a range of indices to an (R, G, B) color tuple.

		:param key: an index or range of indices to set
		:param color:   an (R, G, B) color value
		"""

		if isinstance(key, slice):
			thetaRange = key.start
			phiRange   = key.stop

			self.fill(color, thetaRange, phiRange)

		elif isinstance(key, int):
			raise NotImplementedError('Int as index')

		elif isinstance(key, tuple) or isinstance(key, list):
			self._strip[key] = color

		else:
			raise TypeError('Invalid Argument Type: {}'.format(type(key)))

		return