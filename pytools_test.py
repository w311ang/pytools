import pytools
import os

qpass=os.getenv('qpass')
qfrom=os.getenv('qfrom')
pytools.update(qpass=qpass,qfrom=qfrom)
def qmail_test():
  test1=pytools.qmail('pytools_test','pytools_test','pytools_test')
  assert test1==None
