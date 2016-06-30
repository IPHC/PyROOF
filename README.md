PyROOF
======

A PROOF-like package in Python that read ROOT trees, apply selections and compute variables, and save lighter 'babyTuples' trees.

Workflow
--------

![Workflow sketch](./doc/workflow.png)

Dependencies
------------

You will need `rootpy` installed. NB : you need to do this only once, you can check if you already installed `rootpy` by doing `ls ~/.local/lib/python*/site-packages`.

```
git clone git://github.com/rootpy/rootpy.git
cd rootpy
python setup.py install --user
cd ..
```

If the `python setup.py ...` complains, you might have to install setuptools :

```
wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py
python ez_setup.py --user
```

Then retry from the `python setup.py ...` step.

(Full instructions [here](http://www.rootpy.org/install.html))

Install
-------

Clone this repository :

```
git glone https://github.com/IPHC/PyROOF.git
```

Usage
-----

Plug your analysis selection, babyTuple format, variables and datasets in `analysis/yourAnalysis`, e.g. :

```
git clone https://github.com/oneLeptonStopAt13TeV/phys14Selection.git analysis/stopPhys14
```

And change the analysis name in `config/config.py`.

For further configuration, you may look in the `/config/` folder, in particular `localMultiprocessing.py` and `pbsMultiprocessing.py` allow you to configure for instance the number of workers and the output directory.

To get help about options (to launch in debug mode, local multiprocessing or PBS/batch mode), type

```
./PyROOF.py --help
```


New features
----

- Add a new mode to run on a give root-file and select it at execution time - passed as arguments in the command line - option: -O datasetname rootfile-path


Temporary modifications
----
- Change the name of the tree in processors/kirillFlatTree.py to copte with new temporaty production



Todo
----

- Automatically timestamp output folder ?
- Option to run only on n% of the dataset files ?
- Display run time + time per event at the end of execution ?
- Be able to choose number of file per job in PBS mode
- Check compression usage in kirill's flat tree when opening the tree
