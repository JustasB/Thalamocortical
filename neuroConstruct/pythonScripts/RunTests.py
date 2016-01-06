# -*- coding: utf-8 -*-
#
#
#   File to test cells in Thalamocortical project.
#
#   To execute this type of file, type '..\..\..\nC.bat -python XXX.py' (Windows)
#   or '../../../nC.sh -python XXX.py' (Linux/Mac). Note: you may have to update the
#   NC_HOME and NC_MAX_MEMORY variables in nC.bat/nC.sh
#
#   NOTE: many of the cells will not match well between NEURON, GENESIS and MOOSE
#   until the spatial discretisation (maxElecLens below) is made finer and the
#   simDt is made smaller!!
#
#   Author: Padraig Gleeson
#
#   This file has been developed as part of the neuroConstruct project
#   This work has been funded by the Medical Research Council and the
#   Wellcome Trust
#
#

import sys
import os

try:
    from java.io import File
except ImportError:
    print "Note: this file should be run using ..\\..\\..\\nC.bat -python XXX.py' or '../../../nC.sh -python XXX.py'"
    print "See http://www.neuroconstruct.org/docs/python.html for more details"
    quit()

sys.path.append(os.environ["NC_HOME"]+"/pythonNeuroML/nCUtils")

import ncutils as nc # Many useful functions such as SimManager.runMultipleSims found here
from ucl.physiol.neuroconstruct.hpc.mpi import MpiSettings
from java.lang.management import ManagementFactory


projFile = File(os.getcwd(), "../Thalamocortical.ncx")



##############  Main settings  ##################

mpiConfig =               MpiSettings.MATLEM_1PROC
mpiConfig =               MpiSettings.LOCAL_SERIAL

simConfigs = []

simConfigs.append("Default Simulation Configuration")

##########################################################################
#
#          Note: any of the sim configs below will need a small dt and
#          a fine spatial discretisation (maxElecLens) to have a close
#          match between NEURON, MOOSE & GENESIS
#
#simConfigs.append("Cell1-supppyrRS-FigA1RS")
simConfigs.append("Cell2-suppyrFRB-FigA1FRB")   # use maxElecLens = 0.01
#simConfigs.append("Cell3-supbask-FigA2a")
simConfigs.append("Cell4-supaxax-FigA2a")
#simConfigs.append("Cell5-supLTS-FigA2b")
#simConfigs.append("Cell6-spinstell-FigA3-333")
#simConfigs.append("Cell7-tuftIB-FigA4-1500")
#simConfigs.append("Cell8-tuftRS-Fig5A-1400")
#simConfigs.append("Cell9-nontuftRS-FigA6-1000")
#simConfigs.append("Cell12-deepLTS-FigA2b")
#simConfigs.append("Cell13-TCR-FigA7-600")
simConfigs.append("Cell14-nRT-FigA8-00")
#
##########################################################################

simDt =                 0.005

neuroConstructSeed =    12345
simulatorSeed =         11111
simulators =            ["NEURON", "GENESIS_PHYS",  "MOOSE_PHYS", "MOOSE_SI"]  #"GENESIS_SI",
simulators =            ["NEURON", "GENESIS_PHYS"]  #"GENESIS_SI",
#simulators =            ["GENESIS", "MOOSE"]
#simulators =            ["NEURON"]


maxElecLens =           [0.01]  # 0.01 will give ~700 in FRB & RS
#maxElecLens =            [-1]  # -1 means don't recompartmentalise use settings in proj
#maxElecLens =           [0.025, 0.01,0.005, 0.0025, 0.001,0.0005, 0.00025, 0.0001]

numConcurrentSims =     ManagementFactory.getOperatingSystemMXBean().getAvailableProcessors() -1

if mpiConfig != MpiSettings.LOCAL_SERIAL: 
  numConcurrentSims = 60
suggestedRemoteRunTime = 80   # mins

varTimestepNeuron =     False  # could be more accurate with var time step in nrn, but need to compare these to jNeuroML_NEURON
varTimestepTolerance =  0.00001

analyseSims =           True
plotSims =              True
plotVoltageOnly =       True


simAllPrefix =          ""   # Adds a prefix to simulation reference

runInBackground =       True #(mpiConf == MpiSettings.LOCAL_SERIAL)

suggestedRemoteRunTime = 233

verbose =               True

#############################################


def testAll(argv=None):
    if argv is None:
        argv = sys.argv

    print "Loading project from "+ projFile.getCanonicalPath()


    simManager = nc.SimulationManager(projFile,
                                      numConcurrentSims = numConcurrentSims,
                                      verbose = verbose)

    simManager.runMultipleSims(simConfigs =              simConfigs,
                               simDt =                   simDt,
                               simulators =              simulators,
                               runInBackground =         runInBackground,
                               varTimestepNeuron =       varTimestepNeuron,
                               varTimestepTolerance =    varTimestepTolerance,
                               mpiConfig =               mpiConfig,
                               suggestedRemoteRunTime =  suggestedRemoteRunTime)

    simManager.reloadSims(plotVoltageOnly =   plotVoltageOnly,
                          plotSims =          plotSims,
                          analyseSims =       analyseSims)
                          
    report= ""

    if "Default Simulation Configuration" in simConfigs:
      
      # These were discovered using analyseSims = True above.
      # They need to hold for all simulators
      spikeTimesToCheck = {'CG_CML_0': nc.loadMepFile('.test.mep')['Current clamp']}

      spikeTimeAccuracy = 0.0751  # could be more accurate with var time step in nrn, but need to compare these to jNeuroML_NEURON

      report0 = simManager.checkSims(spikeTimesToCheck = spikeTimesToCheck,
				    spikeTimeAccuracy = spikeTimeAccuracy)

      print report0
      report = report + report0+"\n"
    
    if "Cell2-suppyrFRB-FigA1FRB" in simConfigs:
	
      # These were discovered using analyseSims = True above.
      # They need to hold for all simulators
      spikeTimesToCheck = {'CGsuppyrFRB_0': nc.loadMepFile('.test.l23frb.mep')['L23FRB']}

      spikeTimeAccuracy = 2.32 #  # could be more accurate with var time step in nrn, but need to compare these to jNeuroML_NEURON

      report2 = simManager.checkSims(spikeTimesToCheck = spikeTimesToCheck,
				    spikeTimeAccuracy = spikeTimeAccuracy)

      print report2
      report = report + report2+ '\n'
      
    if "Cell4-supaxax-FigA2a" in simConfigs:
	
      spikeTimesToCheck = {'CGsupaxax_0': nc.loadMepFile('.test.supaxax.mep')['SupAxAx']}

      spikeTimeAccuracy = 0.711 # ms # could be more accurate with var time step in nrn, but need to compare these to jNeuroML_NEURON

      report2 = simManager.checkSims(spikeTimesToCheck = spikeTimesToCheck,
				    spikeTimeAccuracy = spikeTimeAccuracy)

      print report2
      report = report + report2+"\n"
      
    if "Cell14-nRT-FigA8-00" in simConfigs:
	
      spikeTimesToCheck = {'CGnRT_0': nc.loadMepFile('.test.nrt.mep')['nRT']}

      spikeTimeAccuracy = 0.271 # ms  # could be more accurate with var time step in nrn, but need to compare these to jNeuroML_NEURON

      report2 = simManager.checkSims(spikeTimesToCheck = spikeTimesToCheck,
				    spikeTimeAccuracy = spikeTimeAccuracy)

      print report2
      report = report + report2+"\n"
      

    return report


if __name__ == "__main__":
    testAll()
