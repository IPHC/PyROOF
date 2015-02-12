
import analysis

##########################
# WMS task configuration #
##########################

taskName="wmsTask"
corePackage="https://github.com/alexAubin/flatTreeAnalysis"

##########################

from core import WMStaskCreator

createWMStask = WMStaskCreator.createWMStask

def main() :
    createWMStask(taskName,corePackage,analysisName,processorName)
