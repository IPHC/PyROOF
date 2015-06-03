import subprocess

def pbsStatus(dataset_idlist):
    #dataset_summary  = {}
    #print dataset_idlist
    
    # create a summmary of dataset jobs
    dataset_summary = {key:{'R':0, 'Q':0, 'H':0, 'A':len(value)} for key, value  in dataset_idlist.iteritems()}

    username = subprocess.check_output("whoami", shell=True)
    result = subprocess.check_output("qstat -u " + username, shell=True)
    print result
    lines = result.split('\n')
    for line in lines:
        list = line.split()
	print len(list)
	if len(list)==11:
	    #print "job ", list[0] , " Running ?", list[9]
	    for dataset, value in dataset_idlist.iteritems():
	    	for jid in value:
	            if jid[0].split('\n')[0] == list[0]:
		        if list[9] == "R":
		            dataset_summary[dataset]['R'] +=1
		        if list[9] == "Q":
		            dataset_summary[dataset]['Q'] +=1
		        if list[9] == "H":
		            dataset_summary[dataset]['H'] +=1

	

    # compute the list fraction of jobs process per datasets
    allRunning = 0
    allFinished = 0
    allJobs = 0
    
    # return jobStatus per dataset (True if all jobs are ended
    jobStatus = {}

    for dataset, value in dataset_idlist.iteritems():
        print dataset_summary[dataset]['A'], dataset_summary[dataset]['R'], dataset_summary[dataset]['Q'], dataset_summary[dataset]['H']
        finished = dataset_summary[dataset]['A']-dataset_summary[dataset]['R']-dataset_summary[dataset]['Q']-dataset_summary[dataset]['H']
        allFinished+=finished
	allJobs+=dataset_summary[dataset]['A']
	print "Dataset = ", dataset,  'finished  = ', finished, " / ", dataset_summary[dataset]['A'], " running = ", dataset_summary[dataset]['R']
	allRunning+=dataset_summary[dataset]['R']

        if finished == dataset_summary[dataset]['A']:
	    jobStatus[dataset] = True
	else:
	    jobStatus[dataset] = False

    # compute the total number of running jobs
    print "Total number of running jobs:   ", allRunning
    print "Total number of finished jobs:  ", allFinished, " / ", allJobs

    
    return jobStatus

