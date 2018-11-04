#!/opt/anaconda/anaconda2/bin/python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
import random
import numpy as np

class gspread_io:
  _scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
  def __init__(self, cred_fname, sp_name):
    print 'cred_fname = %s, sp_name = %s' %(cred_fname, sp_name)
    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_fname, self._scope)
    self._gc = gspread.authorize(credentials)
    self._sp = self._gc.open(sp_name)

  def add_table(self, sheet_name, table):
    if sheet_name == None:
      print "sheet_name = %s passed. Returning" % sheet_name
      return
    
    num_rows = len(table)
    num_cols = len(table[0])
    if num_cols > 26:
      print 'only <= 26 columns are supported for now. sheet_name = %s, num_cols = %d' % (sheet_name, num_cols)
      return
    
    try:
      sht = self._sp.worksheet(sheet_name)
      print 'Update existing worksheet %s' % sheet_name
    except:
      sht =self._sp.add_worksheet(sheet_name, rows='100', cols='20')
      print 'Add new worksheet %s' % sheet_name

    cell_range = '{col_i}{row_i}:{col_f}{row_f}'.format(
                  col_i=chr((1-1) + ord('A')),    # converts number to letter
                  col_f=chr((num_cols-1) + ord('A')),      # subtract 1 because of 0-indexing
                  row_i=1,
                  row_f=num_rows)
    print 'write to cell_range=%s' % cell_range

    cells = sht.range(cell_range)
    for cell in cells:
      cell.value = table[cell.row-1][cell.col-1]
    
    sht.update_cells(cells)

    print "updated sheet %s" % sheet_name

def main():
  g = gspread_io(sys.argv[1], 'testproject_spreadsheet')

  g.add_table('sheet2', np.random.randint(100, size=(3,4)))
  

if __name__ == '__main__':
  main()


