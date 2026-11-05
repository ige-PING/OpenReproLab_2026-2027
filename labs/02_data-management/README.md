This content is released under the terms of the [Creative Commons Attribution Share Alike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/).

# Part 0: Ressources

An awesome list of useful ressources (articles, presentations, tutorials) to make you aware of the FAIR and open data management in research :

all : https://earth-env-data-science.github.io/lectures/data.html

## FAIR principles

- original paper : https://www.nature.com/articles/sdata201618
- all FAIR principles in one page : https://www.gofair.foundation/fair-principles or one video https://www.youtube.com/watch?v=2uZxFu9SFi8
- some extra explanations (in French) : https://www.inist.fr/wp-content/uploads/2026/04/Webinaire_PrincipesFAIR-CycleDeVie_2026.pdf 
- how to implement the principles and some checklist to achieve it : https://guides.library.cmu.edu/researchdatamanagement/FAIR_principles

## Data format and conventions

- python libraries for various data format :
  - ascii/txt : https://docs.python.org/fr/3/tutorial/inputoutput.html#reading-and-writing-files, https://numpy.org/doc/stable/reference/generated/numpy.loadtxt.html
  - csv/xlsx : https://pandas.pydata.org/docs/user_guide/10min.html#
  - spatial data : https://annefou.github.io/metos_python/02-formats/, https://docs.xarray.dev/en/stable/user-guide/index.html, https://tutorial.xarray.dev/intro.html
  
- netcdf : (french) : https://www.odatis-ocean.fr/fileadmin/documents/activites/ateliers/atelier_201910/201910_ODATIS_Atelier_JSudre_netcdf.pdf  https://sist.pages.in2p3.fr/webinaire_netcdf_2024/introduction.html#, conventions : https://sist.pages.in2p3.fr/webinaire_netcdf_2024/conventions.html 
- CF conventions : https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html

## Data warehouses

- dataterra (thematic) : ocean = odatis (french) : https://www.odatis-ocean.fr/fileadmin/documents/activites/webinaire/202510_CafeODATIS_entrepots.pdf, atmosphere = aeris : https://www.aeris-data.fr/, glacier = theia : https://www.theia-land.fr/
- zenodo (generic) : https://help.zenodo.org/docs/deposit/create-new-upload/ 
- recherchedatagouv (generic) : https://recherche.data.gouv.fr/en/page/tutorial-depositing-a-dataset
  
# Part 1: FAIR principles

Part 1 of this lab is a short multiple-choice questionnaire on FAIR principles : [questionnaire-on-licenses.md](./questionnaire-on-fair.md). Select the correct answer(s) by adding a lower-case x in the corresponding boxes. Push the update file to Github/Gitlab to check your answers.

# Part 2: Data format, metadata and conventions

Part 2 of this lab is an exploration of some data formats that are used at IGE and the python librairies associated that can be useful to read or write data in this format, keeping in mind that the more self-describing the data are, the better.

Open and fill out the [data-format notebook](./data-format.ipynb) and push the update file to Github/Gitlab to check your answers.

# Part 3: Data warehouses

Use the [sandbox of zenodo](https://sandbox.zenodo.org/) to host a data file of your own that follows at best the FAIR principles and provide a "fake" doi for it. Generate a link for your data and put it in [this file](zenodo-sandbox-link.md) so we can check it is a valid zenodo sandbox upload