
export LD_PRELOAD=/usr/lib64/libglobus_gssapi_gsi.so.4

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

mkdir sandbox
cd sandbox

echo " "
echo "> Setting up environment"
echo "(" `date` ")"
echo " "

source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel CMSSW_$CMSSW_VERSION
cd CMSSW_$CMSSW_VERSION/src
cmsenv
cd ../..
git clone $ANALYSIS_PACKAGE analysisPackage
cd analysisPackage

echo " "
echo "> Starting task"
echo "(" `date` ")"
echo " "
#python tools/wmsWorker.py $USER_NAME $DATASET_NAME $INPUT_FILE
echo $USER_NAME $DATASET_NAME $INPUT_FILE > out.txt

echo " "
echo "> Copying output"
echo "(" `date` ")"
echo " "
srmcp -overwrite_mode=ALWAYS -retry_num 4 -retry_timeout 30000 file:///$PWD/out.txt srm://sbgse1.in2p3.fr:8446/${OUTPUT_DIRECTORY}/out.txt

echo " "
echo "> Cleaning environment"
echo " "
cd ../../../
rm -rf sandbox

END_TIME=$(date) 
END_TIME_S=$(date +"%s") 
DURATION=$(($END_TIME_S - $START_TIME_S))
echo " "
echo "======================="
echo "       Job ending      "
echo "                       "
echo "End time : $END_TIME   "
echo "Duration : $DURATION   "
echo "======================="
echo " "

