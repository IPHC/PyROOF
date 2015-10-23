#!/bin/bash
#PBS -e ERRFILE
#PBS -o LOGFILE

START_TIME=$(date) 
START_TIME_S=$(date +"%s") 
echo " "
echo "========================="
echo "       Beginning job     "
echo "                         "
echo "Start time : $START_TIME "
echo "Hostname   : $HOSTNAME   "
lsb_release -a
echo "========================="
echo " "

######################
# Set up environment #
######################
echo " "
echo "> Setting up environment"
echo "(" `date` ")"
echo " "

#export LD_PRELOAD=/usr/lib64/libglobus_gssapi_gsi.so.4
export V0_CMS_SW_DIR=/cvmfs/cms.cern.ch/
source $V0_CMS_SW_DIR/cmsset_default.sh

# Grid/DPM proxy
# --------------

export X509_USER_PROXY=/home-pbs/$USER/.dpmProxy

# LD_LIBRARY_PATH
# ---------------

#CMSSW_ENV="7_4_12_patch4"
CMSSW_ENV="7_4_12"
#PATCH="-patch"
PATCH=""

#export LD_LIBRARY_PATH=\
#/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gcc/4.9.1-cms/lib64/:\
#/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gcc/4.9.1-cms/lib:\
#/usr/lib64:\
#/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw${PATCH}/CMSSW_${CMSSW_ENV}/external/slc6_amd64_gcc491/lib/:\
#/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw${PATCH}/CMSSW_${CMSSW_ENV}/lib/slc6_amd64_gcc491/:\
#/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_12/lib/slc6_amd64_gcc491/:\
#$LD_LIBRARY_PATH

# Python 2.7.6
# ------------

export PATH=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw${PATCH}/CMSSW_${CMSSW_ENV}/external/slc6_amd64_gcc491/bin:\
/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw${PATCH}/CMSSW_${CMSSW_ENV}/bin/slc6_amd64_gcc491/:\
/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_12/bin/slc6_amd64_gcc491:\
/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gcc/4.9.1-cms/bin:\
$PATH
export PYTHONDIR=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/python/2.7.6-cms
export LD_LIBRARY_PATH=$PYTHONDIR/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/home-pbs/$USER/.local/:$ROOTSYS/lib:$PYTHONPATH

# ROOT 5.34
# ---------

source /cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw${PATCH}/CMSSW_${CMSSW_ENV}/external/slc6_amd64_gcc491/bin/thisroot.sh
export LD_LIBRARY_PATH=$ROOTSYS/lib:$LD_LIBRARY_PATH



#############################
# Setup CMSSW environnement #
#############################


export SCRAM_ARCH=slc6_amd64_gcc491
export V0_CMS_SW_DIR=/cvmfs/cms.cern.ch/
source $V0_CMS_SW_DIR/cmsset_default.sh




############################################
# Move to working area and launch analysis #
############################################

echo " "
echo "> Moving to working area"
echo "(" `date` ")"
echo " "

# To be replaced by job creater/submitter
MOVE_TO_WORKING_AREA
#cmsenv
scram runtime -sh

#PYTHONPATH=$PYTHONPATH:$PWD

echo " "
echo "> Launch the analysis"
echo "(" `date` ")"
echo " "

# To be replaced by job creater/submitter
LAUNCH_PYTHON_SCRIPT

######################
# End of job message #
######################

END_TIME=$(date) 
END_TIME_S=$(date +"%s") 
DURATION=$(($END_TIME_S - $START_TIME_S))
echo " "
echo "======================="
echo "       Job ending      "
echo "                       "
echo "End time : $END_TIME   "
echo "Duration : $(($DURATION / 60)) min $(($DURATION % 60)) s "
echo "======================="
echo " "
