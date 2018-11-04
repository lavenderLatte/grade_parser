#!/opt/anaconda/anaconda2/bin/python
import sys
import os

class grade_parser:
  def __init__(self, dir_name=None):
    if dir_name == None:
      dir_name = os.curdir()
    
