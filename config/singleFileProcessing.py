from config import config

# ##################
# #  Initial call  #
# ##################

def main(idataset, ifile) :

    if (idataset >= len(config.datasets) ) :
        print "This dataset does not exist (no = ", idataset, ")"
	return

    # Load only first dataset
    config.datasets[idataset].load(config.processor.getNumberOfInitialEvents)

    # Launch analyzer of first file of first dataset
    if ifile >= len(config.datasets[idataset].files):
        print "This file does not exist (no = ", ifile, ")"
    config.processor.treeProcess(config.datasets[idataset].files[ifile], config.analyzer, "output.root", config.datasets[idataset])


