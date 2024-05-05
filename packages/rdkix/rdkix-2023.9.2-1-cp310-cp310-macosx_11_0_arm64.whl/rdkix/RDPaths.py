import os
# unset so to trigger exceptions and track use: RDBaseDir=os.environ['RDBASE']
RDCodeDir=os.path.join(r'/Users/runner/work/rdkix-pypi/rdkix-pypi/build/temp.macosx-11.0-arm64-cpython-310/rdkix_install/lib/python3.10/site-packages','rdkix')
# not really hard-coded alternative RDCodeDir=os.path.dirname(__file__)
_share = os.path.dirname(__file__)
RDDataDir=os.path.join(_share,'Data')
RDDocsDir=os.path.join(_share,'Docs')
RDProjDir=os.path.join(_share,'Projects')
RDContribDir=os.path.join(_share,'Contrib')
