# Flattree Analysis

A framework to analyze flat ROOT trees to produce lighter 'babyTuples' trees.

Workflow
--------

![Workflow sketch](./workflow.png)

Install and usage
-----------------

You will need `rootpy` installed somewhere. (Full instructions [here](http://www.rootpy.org/install.html))

```
git clone git://github.com/rootpy/rootpy.git
cd rootpy
python setup.py install --user
cd ..
```

Clone this repository :

```
git glone https://github.com/alexAubin/flatTreeAnalysis.git
```

Then plug your analysis selection, babyTuple format, variables and datasets in `analysis/yourAnalysis`, e.g. :

```
git clone https://github.com/oneLeptonStopAt13TeV/phys14Selection.git analysis/stopPhys14
```

In the `/config/` folder, `config.py`, `localMultiprocessing.py` and `wmsTaskCreator.py` allow you to configure how you want things to be done, such as which analysis to use (in the previous example, stopPhys14). Then from `launch.py`, you can choose wether your want to run using debugging mode, local multiprocessing or WMS jobs.
