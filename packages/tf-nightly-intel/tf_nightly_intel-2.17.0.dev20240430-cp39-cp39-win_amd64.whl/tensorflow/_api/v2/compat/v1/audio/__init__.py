# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.audio namespace
"""

import sys as _sys

from tensorflow.python.ops.gen_audio_ops import decode_wav # line: 162
from tensorflow.python.ops.gen_audio_ops import encode_wav # line: 302

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "audio", public_apis=None, deprecation=True,
      has_lite=False)
