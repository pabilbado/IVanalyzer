# IVanalyzer 
The main function of this project is to create a program that can be employed to run an SR830 with an Agilent Source in order to perform a Low noise analysis of the IV and IR characteristic of a sample.


# Installation
You need to install HDF5 : https://www.hdfgroup.org/

TeX Live : https://tug.org/texlive/

pdfTeX : https://www.tug.org/applications/pdftex/

And the rest can be installed employing pip. For that run 

$pip install req.txt

If any more dependencies are missing install them manually.

## Run
You can run two different modes, "main.py" which will perform the measurements and create a pdf employing LaTex as a logbook.

And "analyse.py" that will analyse the results within the results folder. It will classify the files in different diameters by default, but the tag that classifies the data based upon can be changed.
