#
#  Copyright (C) 2004  Rational Discovery LLC
#    All Rights Reserved
#
from rdkix import rdBase

try:
  from rdkix.SimDivFilters import rdSimDivPickers
  from rdkix.SimDivFilters.rdSimDivPickers import *
except ImportError:
  rdSimDivPickers = None
