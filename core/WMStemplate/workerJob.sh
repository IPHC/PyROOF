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
git clone $CORE_PACKAGE analysisPackage
cd analysisPackage

echo " "
echo "> Content of PWD"
echo "(" `date` ")"
echo " "

ls -la

echo " "
echo "> Starting task"
echo "(" `date` ")"
echo " "
#python tools/wmsWorker.py $USER_NAME $DATASET_NAME $INPUT_FILE
echo $USERNAME $DATASET_NAME $INPUT_FILE > out.txt
ls -la
cat out.txt

echo " "
echo "> Copying output"
echo "(" `date` ")"
echo " "
SOURCE="file:///$PWD/out.txt"
DESTINATION="srm://sbgse1.in2p3.fr:8446/${OUTPUT_DIRECTORY}/out.txt"
echo "Source : $SOURCE"
echo "Dest   : $DESTINATION"
srmcp -overwrite_mode=ALWAYS -retry_num 4 -retry_timeout 30000 $SOURCE $DESTINATION 

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
echo "Duration : $(($DURATION / 60)) min $(($DURATION % 60)) s "
echo "======================="
echo " "

