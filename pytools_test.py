import pytools
import os

@pytest.mark.skip(reason='out-of-date api')
def test_passing():
  qpass=os.getenv('qpass')
  qfrom=os.getenv('qfrom')
  pytools.update(qpass=qpass,qfrom=qfrom)
  qmail_test=pytools.qmail('pytools_test','pytools_test','pytools_test')
  assert qmail_test==None

def test_passing():
  jmail_test=pytools.jmail('pytools_test','pytools_test','pytools_test')
  assert jmail_test==None
