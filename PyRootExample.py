import ROOT as r
r.gROOT.LoadMacro("giordon.h+")
from numpy import save
from optparse import OptionParser

parser = OptionParser()

parser.add_option("--inputDir", help="Directory containing input files",type=str, default="JZ1_EM_ClusterInfo")
parser.add_option("--submitDir", help="Directory containing output files",type=str, default=".")
parser.add_option("--numEvents", help="How many events to include (set to -1 for all events)",type=int, default=100000)
parser.add_option("-i","--identifier", help="sample identifier",type=str, default="jz1_EM")

(options, args) = parser.parse_args()

import pdb
def readRoot():

  import glob
  filenamebase = '/u/at/acukierm/nfs/Voronoi_xAOD/JetLearningOut/'
  #filenamebase = '/u/at/acukierm/nfs/Voronoi_xAOD/test/'
  filenamemiddle = '/fetch/data-outputTree/'
  #filenamemiddle = '/data-outputTree/'
  #filenames = glob.glob(filenamebase+options.inputDir+filenamemiddle+'/sample-*.root')
  filenames = glob.glob(filenamebase+options.inputDir+filenamemiddle+'/sample-0.root')
  tree = r.TChain('oTree')
  for filename in filenames:
    #statinfo = os.stat(filename)
    #if statinfo.st_size < 10000: continue #sometimes batch jobs fail
    print '== Reading in '+filename+' =='
    tree.Add(filename) 

  j0pt_arr = []

  #j0_cleta_branch = r.std.vector(r.std.vector('double'))()
  #tree.SetBranchAddress("j0_cleta",j0_cleta_branch)
  nentries = tree.GetEntries()
  print 'Number of events: '+str(nentries)
  for jentry in xrange(nentries):
      if jentry==options.numEvents: break
      tree.GetEntry(jentry)
      j0_clpt_branch = getattr(tree,'j0_clpt')
      print j0_clpt_branch[0][0]
      j0pt_branch = getattr(tree,'jnoarea0pt')
      j0_cleta_branch = getattr(tree,'j0_cleta')
      j0eta_branch = getattr(tree,'j0eta')
      j0_clphi_branch = getattr(tree,'j0_clphi')
      j0phi_branch = getattr(tree,'j0phi')
      print 'Event '+str(tree.event_number)
      for cl_pts,j0pt,cl_etas,j0eta,cl_phis,j0phi in zip(j0_clpt_branch,j0pt_branch,j0_cleta_branch,j0eta_branch,j0_clphi_branch,j0phi_branch):
        print 'Jet: '+str(j0pt)+','+str(j0eta)+','+str(j0phi)
        j0pt_arr.append(j0pt)
        for cl_pt,cl_eta,cl_phi in zip(cl_pts,cl_etas,cl_phis):
          print 'Cluster: '+str(cl_pt)+','+str(cl_eta)+','+str(cl_phi)

  save(options.submitDir+'/recopts_j0_'+options.identifier,j0pt_arr)

readRoot()
