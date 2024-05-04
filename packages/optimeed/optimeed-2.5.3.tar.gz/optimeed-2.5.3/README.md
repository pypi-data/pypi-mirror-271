Optimeed aims at easing data generation and visualization.
Its key strength is its adaptability to _any_ problem thanks to its flexibility, while accounting for parallelization, disk space and RAM usages.

It is divided in 4 Modules:
* `core` Embeds all the tools to load/save python objects in plain text using json-like format.
* `optimize` A framework to solve optimization problem, while profiting from `core` saving utilities.
* `consolidate` A framework to perform sensitivity analyses, while profiting from `core` saving utilities.
* `visualize` A framework for data analysis. Provides GUI for `optimize` and `consolidate`, using 2D interactive graphs. For the optimization, results can be displayed in real time.

<!--
**Requirements**

* PyQt5 for visualisation -> `pip install PyQt5`
* `pyopengl` for visualisation -> `pip install PyOpenGL`
* Numpy -> `pip install numpy`
* Optional
    * pandas which is only used to export excel files -> `pip install pandas`
    * `nlopt` library for using other types of algorithm. -> `pip install nlopt`
    * inkscape software for exporting graphs in .png and .pdf)
    * `plotly` library for 3D plots. -> `pip install plotly`
-->

**Installation**

To install the latest optimeed release, run the following command:

    pip install optimeed

To install the latest development version of optimeed, run the following commands:

    git clone https://git.immc.ucl.ac.be/chdegreef/optimeed.git
    cd optimeed
    python setup.py install

**Support**

Gitlab (preferably), read [the guided tutorials](https://git.immc.ucl.ac.be/chdegreef/optimeed/-/tree/dev/tutorials).

or

[Documentation optimeed](https://optimeed.readthedocs.io/en/latest/)

or

Send mail at christophe.degreef@uclouvain.be.

**License**

The project is distributed "has it is" under [GNU General Public License v3.0 (GPL)](https://www.gnu.org/licenses/gpl-3.0.fr.html), which is a strong copyleft license.
This means that the code is open-source and you are free to do anything you want with it, **as long as you apply the same license to distribute your code**.
This constraining license is imposed by the use of [Platypus Library](https://platypus.readthedocs.io/en/docs/index.html) as "optimization algorithm library", which is under GPL license.

It is perfectly possible to use other optimization library (which would use the same algorithms but with a different implementation) and to interface it to this project, so that the use of platypus is no longer needed. This work has already been done for [NLopt](https://nlopt.readthedocs.io/en/latest/), which is under MIT license (not constraining at all).
In that case, **after removing all the platypus sources** (optiAlgorithms/multiObjective_GA and optiAlgorithsm/platypus/*), the license of the present work becomes less restrictive: [GNU Lesser General Public License (LGPL)](https://www.gnu.org/licenses/lgpl-3.0.html). As for the GPL, this license makes the project open-source and free to be modified, but (nearly) no limitation is made to distribute your code.
