# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.math namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v1.math import special
from tensorflow.python.ops.gen_array_ops import invert_permutation # line: 5406
from tensorflow.python.ops.gen_math_ops import acosh # line: 243
from tensorflow.python.ops.gen_math_ops import asin # line: 1068
from tensorflow.python.ops.gen_math_ops import asinh # line: 1182
from tensorflow.python.ops.gen_math_ops import atan # line: 1282
from tensorflow.python.ops.gen_math_ops import atan2 # line: 1396
from tensorflow.python.ops.gen_math_ops import atanh # line: 1506
from tensorflow.python.ops.gen_math_ops import betainc # line: 2035
from tensorflow.python.ops.gen_math_ops import cos # line: 2780
from tensorflow.python.ops.gen_math_ops import cosh # line: 2882
from tensorflow.python.ops.gen_math_ops import digamma # line: 3580
from tensorflow.python.ops.gen_math_ops import erf # line: 3887
from tensorflow.python.ops.gen_math_ops import erfc # line: 3984
from tensorflow.python.ops.gen_math_ops import expm1 # line: 4314
from tensorflow.python.ops.gen_math_ops import floor_mod as floormod # line: 4572
from tensorflow.python.ops.gen_math_ops import greater # line: 4671
from tensorflow.python.ops.gen_math_ops import greater_equal # line: 4785
from tensorflow.python.ops.gen_math_ops import igamma # line: 5007
from tensorflow.python.ops.gen_math_ops import igammac # line: 5178
from tensorflow.python.ops.gen_math_ops import is_finite # line: 5496
from tensorflow.python.ops.gen_math_ops import is_inf # line: 5601
from tensorflow.python.ops.gen_math_ops import is_nan # line: 5706
from tensorflow.python.ops.gen_math_ops import less # line: 5811
from tensorflow.python.ops.gen_math_ops import less_equal # line: 5925
from tensorflow.python.ops.gen_math_ops import lgamma # line: 6039
from tensorflow.python.ops.gen_math_ops import log # line: 6225
from tensorflow.python.ops.gen_math_ops import log1p # line: 6326
from tensorflow.python.ops.gen_math_ops import logical_and # line: 6421
from tensorflow.python.ops.gen_math_ops import logical_not # line: 6613
from tensorflow.python.ops.gen_math_ops import logical_or # line: 6703
from tensorflow.python.ops.gen_math_ops import maximum # line: 7087
from tensorflow.python.ops.gen_math_ops import minimum # line: 7365
from tensorflow.python.ops.gen_math_ops import floor_mod as mod # line: 4572
from tensorflow.python.ops.gen_math_ops import neg as negative # line: 7735
from tensorflow.python.ops.gen_math_ops import next_after as nextafter # line: 7821
from tensorflow.python.ops.gen_math_ops import polygamma # line: 7996
from tensorflow.python.ops.gen_math_ops import reciprocal # line: 9061
from tensorflow.python.ops.gen_math_ops import rint # line: 9569
from tensorflow.python.ops.gen_math_ops import segment_max # line: 9853
from tensorflow.python.ops.gen_math_ops import segment_mean # line: 10159
from tensorflow.python.ops.gen_math_ops import segment_min # line: 10315
from tensorflow.python.ops.gen_math_ops import segment_prod # line: 10621
from tensorflow.python.ops.gen_math_ops import segment_sum # line: 10910
from tensorflow.python.ops.gen_math_ops import sin # line: 11551
from tensorflow.python.ops.gen_math_ops import sinh # line: 11651
from tensorflow.python.ops.gen_math_ops import square # line: 13328
from tensorflow.python.ops.gen_math_ops import squared_difference # line: 13420
from tensorflow.python.ops.gen_math_ops import tan # line: 13800
from tensorflow.python.ops.gen_math_ops import tanh # line: 13902
from tensorflow.python.ops.gen_math_ops import unsorted_segment_max # line: 14264
from tensorflow.python.ops.gen_math_ops import unsorted_segment_min # line: 14439
from tensorflow.python.ops.gen_math_ops import unsorted_segment_prod # line: 14606
from tensorflow.python.ops.gen_math_ops import unsorted_segment_sum # line: 14771
from tensorflow.python.ops.gen_math_ops import xlogy # line: 15054
from tensorflow.python.ops.gen_math_ops import zeta # line: 15140
from tensorflow.python.ops.gen_nn_ops import softsign # line: 12929
from tensorflow.python.ops.bincount_ops import bincount_v1 as bincount # line: 190
from tensorflow.python.ops.check_ops import is_non_decreasing # line: 1989
from tensorflow.python.ops.check_ops import is_strictly_increasing # line: 2030
from tensorflow.python.ops.confusion_matrix import confusion_matrix_v1 as confusion_matrix # line: 199
from tensorflow.python.ops.math_ops import abs # line: 360
from tensorflow.python.ops.math_ops import accumulate_n # line: 3981
from tensorflow.python.ops.math_ops import acos # line: 5599
from tensorflow.python.ops.math_ops import add # line: 3840
from tensorflow.python.ops.math_ops import add_n # line: 3921
from tensorflow.python.ops.math_ops import angle # line: 864
from tensorflow.python.ops.math_ops import argmax # line: 246
from tensorflow.python.ops.math_ops import argmin # line: 300
from tensorflow.python.ops.math_ops import ceil # line: 5429
from tensorflow.python.ops.math_ops import conj # line: 4354
from tensorflow.python.ops.math_ops import count_nonzero # line: 2274
from tensorflow.python.ops.math_ops import cumprod # line: 4244
from tensorflow.python.ops.math_ops import cumsum # line: 4172
from tensorflow.python.ops.math_ops import cumulative_logsumexp # line: 4298
from tensorflow.python.ops.math_ops import divide # line: 441
from tensorflow.python.ops.math_ops import div_no_nan as divide_no_nan # line: 1525
from tensorflow.python.ops.math_ops import equal # line: 1789
from tensorflow.python.ops.math_ops import erfcinv # line: 5399
from tensorflow.python.ops.math_ops import erfinv # line: 5364
from tensorflow.python.ops.math_ops import exp # line: 5496
from tensorflow.python.ops.math_ops import floor # line: 5630
from tensorflow.python.ops.math_ops import floordiv # line: 1633
from tensorflow.python.ops.math_ops import imag # line: 830
from tensorflow.python.ops.math_ops import log_sigmoid # line: 4127
from tensorflow.python.ops.math_ops import logical_xor # line: 1713
from tensorflow.python.ops.math_ops import multiply # line: 476
from tensorflow.python.ops.math_ops import multiply_no_nan # line: 1580
from tensorflow.python.ops.math_ops import ndtri # line: 5383
from tensorflow.python.ops.math_ops import not_equal # line: 1826
from tensorflow.python.ops.math_ops import polyval # line: 5186
from tensorflow.python.ops.math_ops import pow # line: 664
from tensorflow.python.ops.math_ops import real # line: 789
from tensorflow.python.ops.math_ops import reciprocal_no_nan # line: 5258
from tensorflow.python.ops.math_ops import reduce_all_v1 as reduce_all # line: 3030
from tensorflow.python.ops.math_ops import reduce_any_v1 as reduce_any # line: 3136
from tensorflow.python.ops.math_ops import reduce_euclidean_norm # line: 2229
from tensorflow.python.ops.math_ops import reduce_logsumexp_v1 as reduce_logsumexp # line: 3242
from tensorflow.python.ops.math_ops import reduce_max_v1 as reduce_max # line: 2905
from tensorflow.python.ops.math_ops import reduce_mean_v1 as reduce_mean # line: 2428
from tensorflow.python.ops.math_ops import reduce_min_v1 as reduce_min # line: 2777
from tensorflow.python.ops.math_ops import reduce_prod_v1 as reduce_prod # line: 2718
from tensorflow.python.ops.math_ops import reduce_std # line: 2618
from tensorflow.python.ops.math_ops import reduce_sum_v1 as reduce_sum # line: 2071
from tensorflow.python.ops.math_ops import reduce_variance # line: 2555
from tensorflow.python.ops.math_ops import round # line: 909
from tensorflow.python.ops.math_ops import rsqrt # line: 5574
from tensorflow.python.ops.math_ops import scalar_mul # line: 587
from tensorflow.python.ops.math_ops import sigmoid # line: 4074
from tensorflow.python.ops.math_ops import sign # line: 742
from tensorflow.python.ops.math_ops import sobol_sample # line: 5549
from tensorflow.python.ops.math_ops import softplus # line: 629
from tensorflow.python.ops.math_ops import sqrt # line: 5457
from tensorflow.python.ops.math_ops import subtract # line: 540
from tensorflow.python.ops.math_ops import truediv # line: 1459
from tensorflow.python.ops.math_ops import unsorted_segment_mean # line: 4477
from tensorflow.python.ops.math_ops import unsorted_segment_sqrt_n # line: 4532
from tensorflow.python.ops.math_ops import xdivy # line: 5292
from tensorflow.python.ops.math_ops import xlog1py # line: 5326
from tensorflow.python.ops.nn_impl import l2_normalize # line: 540
from tensorflow.python.ops.nn_impl import zero_fraction # line: 620
from tensorflow.python.ops.nn_ops import approx_max_k # line: 5882
from tensorflow.python.ops.nn_ops import approx_min_k # line: 5945
from tensorflow.python.ops.nn_ops import in_top_k # line: 6532
from tensorflow.python.ops.nn_ops import log_softmax # line: 3923
from tensorflow.python.ops.nn_ops import softmax # line: 3910
from tensorflow.python.ops.nn_ops import top_k # line: 5815
from tensorflow.python.ops.special_math_ops import bessel_i0 # line: 253
from tensorflow.python.ops.special_math_ops import bessel_i0e # line: 282
from tensorflow.python.ops.special_math_ops import bessel_i1 # line: 309
from tensorflow.python.ops.special_math_ops import bessel_i1e # line: 338
from tensorflow.python.ops.special_math_ops import lbeta # line: 45

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "math", public_apis=None, deprecation=True,
      has_lite=False)
