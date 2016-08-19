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
export SCRAM_ARCH=slc6_amd64_gcc530

# Grid/DPM proxy
# --------------

export X509_USER_PROXY=/home-pbs/$USER/.dpmProxy

# LD_LIBRARY_PATH
# ---------------

cd /home-pbs/$USER/CMSSW_8_0_7_patch1/src
eval `scramv1 runtime -sh`
cd -

$LD_LIBRARY_PATH

# Python 2.7.6
# ------------

export PATH=/cvmfs/cms.cern.ch/${VERSION}/cms/cmssw/CMSSW_${CMSSW_ENV}/external/${VERSION}/bin:\
/cvmfs/cms.cern.ch/${VERSION}/external/gcc/${GCVersion}/bin:\
$PATH
export PYTHONDIR=/cvmfs/cms.cern.ch/${VERSION}/external/python/${PYTHONVersion}
export PYTHONPATH=/home-pbs/$USER/.local/:$ROOTSYS/lib:$PYTHONPATH

# ROOT 5.34
# ---------

#source /cvmfs/cms.cern.ch/${VERSION}/cms/cmssw/CMSSW_${CMSSW_ENV}/external/${VERSION}/bin/thisroot.sh
source /cvmfs/cms.cern.ch/slc6_amd64_gcc530/lcg/root/6.06.00-ikhhed3/bin/thisroot.sh
export LD_LIBRARY_PATH=$ROOTSYS/lib:$LD_LIBRARY_PATH
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD

#cd /cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_5/src
#eval `scramv1 runtime -sh`
#cd -

#export LD_LIBRARY_PATH=\/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/gcc/5.3.0/lib64/:\
#$LD_LIBRARY_PATH

#source /cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_5/external/slc6_amd64_gcc530/bin/root/thisroot.sh
#export LD_LIBRARY_PATH=$ROOTSYS/lib:$LD_LIBRARY_PATH


############################################
# Move to working area and launch analysis #
############################################

echo " "
echo "> Moving to working area"
echo "(" `date` ")"
echo " "

which root
echo $ROOTSYS
root -l -b --version -q


# To be replaced by job creater/submitter
MOVE_TO_WORKING_AREA
PYTHONPATH=$PYTHONPATH:$PWD
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD

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
