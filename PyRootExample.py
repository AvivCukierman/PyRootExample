import ROOT as r
from optparse import OptionParser

parser = OptionParser()

parser.add_option("--inputDir", help="Directory containing input files",type=str, default="input")
parser.add_option("--submitDir", help="Directory containing output files",type=str, default="output")
parser.add_option("--numEvents", help="How many events to include (set to -1 for all events)",type=int, default=-1)
parser.add_option("-i","--identifier", help="sample identifier",type=str, default="my_analysis")

parser.add_option("--treeName", help="Name of Tree",type=str, default="oTree")
parser.add_option("--jetBranchName", help="Name of sample jet branch",type=str, default="j0pt")
parser.add_option("--clusterBranchName", help="Name of sample cluster branch",type=str, default="j0_clpt")

(options, args) = parser.parse_args()

if options.clusterBranchName: r.gROOT.LoadMacro("giordon.h+") #only necessary if we have vector<vector<...>> information

import pdb
def readRoot():

  import glob
  filenames = glob.glob(options.inputDir+'/*.root')
  print 'Searching for ROOT files in:'
  print options.inputDir+'/*.root'
  if len(filenames)==0: raise IOError('No ROOT files found!')
  tree = r.TChain(options.treeName)
  for filename in filenames:
    #statinfo = os.stat(filename)
    #if statinfo.st_size < 10000: continue #if you want to remove failed jobs
    print '== Reading in '+filename+' =='
    tree.Add(filename) 

  j0pt_arr = []

  nentries = tree.GetEntries()
  print 'Number of events: '+str(nentries)
  for jentry in xrange(nentries):
      if jentry==options.numEvents: break
      tree.GetEntry(jentry)
      print 'Event '+str(tree.event_number)
      j0pt_branch = getattr(tree,options.jetBranchName)
      j0_clpt_branch = getattr(tree,options.clusterBranchName)
      print j0_clpt_branch[0][0]
      for j0pt,cl_pts in zip(j0pt_branch,j0_clpt_branch):
        print 'Jet: '+str(j0pt)
        j0pt_arr.append(j0pt)
        for cl_pt in cl_pts:
          print 'Cluster: '+str(cl_pt)

  #from numpy import save
  #save(options.submitDir+'/recopts_j0_'+options.identifier,j0pt_arr) #to save the information as a numpy array

  return j0pt_arr

jetpt_data = readRoot()
# do whatever
