#PBS -u echabert
#!/bin/bash

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

echo " "
echo "> Setting up environment"
echo "(" `date` ")"
echo " "

#source environment
export LD_PRELOAD=/usr/lib64/libglobus_gssapi_gsi.so.4
export V0_CMS_SW_DIR=/cvmfs/cms.cern.ch/
source $V0_CMS_SW_DIR/cmsset_default.sh

export LD_LIBRARY_PATH=\
/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gcc/4.9.1-cms/lib64:\
/usr/lib64:\
/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gcc/4.9.1-cms/lib:\
/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_1/external/slc6_amd64_gcc491/lib/:\
/cvmfs/cms.cern.ch/slc6_amd64_gcc491/cms/cmssw/CMSSW_7_4_1/lib/slc6_amd64_gcc491/:\
$LD_LIBRARY_PATH
export PATH=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/gcc/4.9.1-cms/bin:/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/python/2.7.6-cms/bin:/opt/sbg/scratch1/cms/echabert/.local/bin:$PATH

#ROOT
source /cvmfs/cms.cern.ch/slc6_amd64_gcc481/lcg/root/5.34.18-cms14/bin/thisroot.sh
export PYTHONDIR=/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/python/2.7.6-cms
export LD_LIBRARY_PATH=$ROOTSYS/lib:$PYTHONDIR/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$ROOTSYS/lib:/opt/sbg/scratch1/cms/echabert/CMSSW_7_3_0/src/PyROOF:/opt/sbg/scratch1/cms/echabert/.local/lib/python2.7/site-packages:$PYTHONPATH

#alias python="/cvmfs/cms.cern.ch/slc6_amd64_gcc491/external/python/2.7.6-cms/bin/"

echo " "
echo "> Move to scratch1 setup"
echo "(" `date` ")"
echo " "

cd /opt/sbg/scratch1/cms/echabert/CMSSW_7_3_0/src/
source /cvmfs/cms.cern.ch/cmsset_default.sh
#cmsenv
#eval `scramv1 runtime -sh`

echo " "
echo "> Launch the analysis"
echo "(" `date` ")"
echo " "

LAUNCH_PYTHON_SCRIPT

########################
# move the output file #
########################

echo " "
echo "> Move the output filep"
echo "(" `date` ")"
echo " "

COPY_OUTPUT_FILE

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
