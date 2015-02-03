
from common import genericDataset

Dataset = genericDataset.Dataset
datasets = [
    Dataset("ttbar",        "./store/FlatTrees/ttbar/*.root",          xsection=-1),
    Dataset("T2tt_850_100", "./store/FlatTrees/T2tt_850_100/*.root",   xsection=-1),
    Dataset("WZ",           "./store/FlatTrees/WZ/*.root",             xsection=-1),
    Dataset("Wjets",        "./store/FlatTrees/Wjets/*.root",          xsection=-1),
    Dataset("singleT-s",    "./store/FlatTrees/singleT-s/*.root",      xsection=-1),
    Dataset("singleT-t",    "./store/FlatTrees/singleT-t/*.root",      xsection=-1),
    Dataset("singleTbar-s", "./store/FlatTrees/singleTbar-s/*.root",   xsection=-1),
    Dataset("singleTbar-t", "./store/FlatTrees/singleTbar-t/*.root",   xsection=-1),
    Dataset("ttW",          "./store/FlatTrees/ttW/*.root",            xsection=-1),
    Dataset("ttZ",          "./store/FlatTrees/ttZ/*.root",            xsection=-1) 
]

