#!/bin/env zsh

#list of directories with files to merge
slist="list.txt"


dir=()
is=1
loc=root://sbgse1.in2p3.fr:1094///dpm/in2p3.fr/home/cms/phedex/store/user
locold=/dpm/in2p3.fr/home/cms/phedex/store/user

#read directories
cat ${slist} | while read line
do
    dir[${is}]=${line}
    is=$[$is+1]
done

for i in ${dir}
do

    #save names of files in tmp file
    /usr/bin/rfdir ${i} | awk '{print $9}' > tmp
    #/usr/bin/rfdir ${i} | awk '{print $5}' > tmp2

    #dpm string to put before file when doing hadd
    t="${i/${locold}/${loc}}"

    f=1

    #read files into array
    cat tmp | while read line
    do
        if [ "${line}" = "failed" ]; then
            continue
        fi
        if [ "${line}" = "merged" ]; then
            continue
        fi
        file[${f}]=${line}
        f=$[$f+1]
    done

    #default or usef defined size of packets
    nr=20 #nr of files to merge (how large the packets will be)
    if [ "$1" != "" ]; then
        nr=$1
    else
        echo "Positional parameter 1 is empty, using default value"
    fi

    counter=1
    iter=1
    arr[${counter}]=hadd" "${t}"/merged/"merged_${counter}.root
    arr2[${counter}]=/usr/bin/rfrm

    #loop over files and prepare hadd and rfrm commands
    for j in ${file} 
    do

        if [ "$iter" -gt  "$(($counter * $nr))" ]; then
            counter=$(($counter + 1))
            arr[${counter}]=hadd" "${t}"/merged/"merged_${counter}.root
            arr2[${counter}]=/usr/bin/rfrm
        fi
        iter=$(($iter + 1))
        arr[${counter}]=${arr[${counter}]}" "${t}"/"${j}
        arr2[${counter}]=${arr2[${counter}]}" "${i}"/"${j}
    done

    pos=1

    #apply hadd and rfrm commands
    for l in "${arr[@]}"
    do
        eval $l
        #echo ${arr2[$pos]} #@MJ@ TODO compare size of input and output and then remove
        pos=$(($pos + 1))     
    done

done

#remove temporary file 
rm tmp
