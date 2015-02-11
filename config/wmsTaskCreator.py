
import analysis

##########################
# WMS task configuration #
##########################

taskName="wmsTask"
commonPackage="https://github.com/alexAubin/flatTreeAnalysis"

##########################

from common import WMStaskCreator

createWMStask = WMStaskCreator.createWMStask

def main() :
    createWMStask(taskName,commonPackage,analysisName,processorName)
