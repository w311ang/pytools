import pytools
import os

qpass=os.getenv('qpass')
qfrom=os.getenv('qfrom')
pytools.update(qpass=qpass,qfrom=qfrom)
def test_passing():
  test1=pytools.qmail('pytools_test','pytools_test','pytools_test')
  assert test1==None
