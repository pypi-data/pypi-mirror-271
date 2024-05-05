# $Id$
#
#  Copyright (C) 2007 Greg Landrum
#   @@ All Rights Reserved @@
#  This file is part of the RDKix.
#  The contents are covered by the terms of the BSD license
#  which is included in the file license.txt, found at the root
#  of the RDKix source tree.
#
import sys
import warnings

from rdkix import Chem

warnings.warn(
  "The FastSDMolSupplier class has been deprecated, please use Chem.SDMolSupplier instead",
  DeprecationWarning)


class FastSDMolSupplier(Chem.SDMolSupplier):
  pass
