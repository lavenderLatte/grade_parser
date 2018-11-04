#!/opt/anaconda/anaconda2/bin/python
import sys
import os
from gspread_io import gspread_io
from dir_parser import dir_parser
import pprint

class grade_parser:
  
  def __init__(self, dir_name=None, gc=None):
    if dir_name == None:
      dir_name = os.getcwd()
    
    self._dir_name = dir_name

    if not os.path.exists(dir_name):
      raise Exception("dir_name = %s is invalid"%dir_name)
    
    self._gc = gc

  def unzip_directories(self):
    print 'Unzipping directories not supported just yet'
    return

  def parse_directories(self):
    for subdir, dirs, _ in os.walk(self._dir_name):
      # print 'subdir=%s, dirs=%s, files=%s'%(subdir, dirs, files)
      if len(dirs) > 0:
        for dir_name in dirs:
          print 'WARNING: skipped directory=%s' % (os.path.join(subdir, dir_name))
      dparser = dir_parser(subdir)
      table = dparser.result_table()
      base_dir_name = os.path.basename(subdir)

      if not self._gc==None:
        self._gc.add_table(base_dir_name, table)
      else:
        print pprint.pprint(table)


def main():
  gc = None
  if len(sys.argv) == 3:
    gc = gspread_io(sys.argv[2], 'testproject_spreadsheet')
  
  g = grade_parser(dir_name=sys.argv[1], gc=gc)
  g.parse_directories() 

if __name__ == '__main__':
  main()   
    
