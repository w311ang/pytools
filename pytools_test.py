import pytools
import os

qpass=os.getenv('qpass')
qfrom=os.getenv('qfrom')
pytools.update(qpass=qpass,qfrom=qfrom)
def test_passing():
  qmail_test=pytools.qmail('pytools_test','pytools_test','pytools_test')
  assert qmail_test==None
def test_passing():
  jmail_test=pytools.jmail('pytools_test','pytools_test','pytools_test')
  assert jmail_test==None
