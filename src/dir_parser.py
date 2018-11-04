#!/opt/anaconda/anaconda2/bin/python
import re
import os
import csv
import sys

class dir_parser:
  
  def __init__(self, dir_name):
    if not os.path.exists(dir_name): raise Exception("dir_name = %s is invalid"%dir_name)
    self._dir_name = dir_name
    self._result_matrix, self._questions = self._get_passing_matrix()
  
  def result_table(self):

    table = [ [" "] + ["total"] + self._questions]
    users = sorted(self._result_matrix.keys())
    for usr in users:
      res = self._result_matrix[usr]
      table.append([usr] + [sum(res)] + res)
    
    return table

  # function to gather passing questions
  # input   -- full file name (i.e., incl. path)
  # output  -- dictionary of passing entries as keys. Values are invalid
  def _get_passing_questions(self, fpath_name):
    # search pattern used to search for passing tests. r at the beginning to indicate raw string.
    # 
    # The search pattern below defines two groups to avoid confusion. 
    # When only one group is defined, findall returns a list of strings that match the pattern in group
    # When >= 2 groups are defined, findall returns list of tuples. Each tuple contains strings -- one for each group
    search_pattern = r"(q\d.*)\.py.*(All tests passed)"

    passed_questions = {}

    #open file
    with open(fpath_name, "rU") as f:
      # read one line at a time. Useful when file could be very large
      for line in f:
        # we expect only one match per line. However, if the input is not as expect, fail
        matches = re.findall(search_pattern, line)
        if(len(matches) > 1): raise Exception('unexpected input. more than 1 match in a line in file %s' % fpath_name)
        
        # there should be <=1 matches. 
        if matches:
          match = matches[0] # there is only one match. 
          passed_questions[match[0]] = "" # first element in the tuple

    return passed_questions


  def _build_sorted_superset(self, usr_results_dict):
    superset_dict = {}
    for val in usr_results_dict.values():
      superset_dict.update(val)

    return sorted(superset_dict.keys())

  def _build_result_matrix(self, usr_results_dict, q_super_set):
    result_matrix = {}

    for usr, res in usr_results_dict.items():
      res_list = []
      for q in q_super_set:
        if q in res : res_list.append(1)
        else        : res_list.append(0)

      print "add usr=%s, res_list=%s"%(usr, res_list)
      result_matrix[usr] = res_list

    return result_matrix

  # function to compute a matrix of passing questions per user
  # input   -- directory with input files (*.ipynb)
  # output  -- 2-tuple.
  #         -- output[0]  --> dictionary mapping user to list of 1 & 0. 
  #         --            --  1 -- question passed, 0 -- question failed.
  #         -- output[1]  --> superset of the list of questions
  #                       --> TODO: list to be user defined/ parsed from notebook file
  #                           --> what if all students do not answer a question?
  def _get_passing_matrix(self):
    usr_results = {}

    files = os.listdir(self._dir_name)
    for file in files:
      # process only files with .ipynb extension
      if not file.endswith(".ipynb"): 
        print "skipping file %s" % file
        continue

      # try to determine username
      usr_name_match = re.search(r'[a-zA-Z0-9]+', file)
      if not usr_name_match: raise Exception("usr_name not found in filename = %s" % file)

      # compute results and associate username with results
      usr_name = usr_name_match.group()
      usr_res = self._get_passing_questions(os.path.join(self._dir_name, file))

      usr_results[usr_name] = usr_res

    sorted_superset_q_list = self._build_sorted_superset(usr_results)

    result_matrix = self._build_result_matrix(usr_results, sorted_superset_q_list)

    return (result_matrix, sorted_superset_q_list)

  def write_results_csv(self, results_fname="results.csv"):
    
    results_fname = os.path.join(self._dir_name, results_fname)

    with open(results_fname, mode="w") as f:
      fwriter = csv.writer(f, delimiter=',')
      
      fwriter.writerow([" "] + self._questions)
      users = sorted(self._result_matrix.keys())
      for usr in users:
        fwriter.writerow([usr] + self._result_matrix[usr])
  
def main():
  d_parser = dir_parser(sys.argv[1])
  table = d_parser.result_table()
  print table


if __name__ == '__main__':
  main()