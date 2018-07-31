# Document similarity measures using tfidf & cosine similarity

This module facilitates the ranking of candidate [PubMed](https://www.ncbi.nlm.nih.gov/pubmed/) articles according to their cosine similarity to a nominated [ClinicalTrials.gov](https://clinicaltrials.gov/)
registry entry

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Requirements

To install and run this example, you will need:
 
 * Git
 * Python 2.7 
 * and virtualenv (which you can install easily using [pip](https://pypi.python.org/pypi/pip))

### Installing

Run the commands below to set everything up such that you will be able to run the script with your own list of PubMed articles
and trial registry entries

```
$ git clone https://github.com/pmartin23/tfidf tfidf
$ virtualenv tfidf
$ tfidf/bin/activate
(tfidf) cd tfidf
(tfidf) pip install -r requirements.txt
```
Note for Microsoft Windows users: replace the virtual environment activation command above with ```tfidf\Scripts\activate```


Once everything is installed, you can run the example with the following command:
```
(tfidf) python -u example.py
```

## Example

The full code for this example can be found in ```example.py```
### Generating the tfidf matrix

First, you'll need to generate and save the tfidf matrix and vectorizer model for the corups of candidate PubMed articles. In this example,
 our features are the terms in the title and abstract of each PubMed article. It may take a while to retrieve all article 
 title & abstract metadata and construct the matrix.

 **Note:** because we save the tfidf matrix and vectorizer to file, we only need to generate these **once** for each set of candidate PubMed articles
```python
from tfidf import gen_tfidf_matrix, docsim

matrix_fname = 'pubmed_tfidf'
vectorizer_fname = 'pmid_vec'
candidate_ids = np.array(['24601174', '19515181', '22512265'])
candidate_docs = [pubmed_text(pmid) for pmid in candidate_ids]  # retrieve text for candidate pubmed articles
gen_tfidf_matrix(candidate_docs, vectorizer_fname, matrix_fname)
```

### Calculating document similarity & ranks
Next, we will calculate the document similarity between each PubMed article and our nominated trial registry entry, using the previously
generated tfidf matrix and vectorizer model. There are two steps in this process, which are implemented in the ```docsim``` method in ```tfidf.py```:
```python
docsim(document, tfidf_vectorizer, tfidf_matrix)
```

* Calculate the tfidf of the registry entry with respect to the features in the corpus of candidate PubMed articles. 
In this example, our features were all terms within the fields 'brief title', 'official title', 'brief summary', 'detailed description', 
and 'condition' of the registry entry metadata.
* Produce a rank for each PubMed article according to its similarity with the registry entry. The similarity is 
determined by calculating the cosine similarity between the vector representing the tfidf of each candidate PubMed article,
and the vector representing the tfidf of the registry entry.

```python
nct_id = 'NCT03132233'
nct_doc = ctgov_text(nct_id)
tfidf_vectorizer = pickle.load(open(vectorizer_fname + ".pickle"))  
tfidf_matrix = scipy.sparse.load_npz(matrix_fname + '.npz') 
ranks = docsim(nct_doc, tfidf_vectorizer, tfidf_matrix)
ranked_pmids = candidate_ids[ranks]
```
We can then see the resulting ranked PubMed articles

```python
print ranked_pmids
... ['22512265' '19515181' '24601174']
```

noting that article with PMID ```22512265``` is most similar to our registry entry with NCT ID ```NCT03132233```


## Authors

* **Adam Dunn** 
* **Paige Martin**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Publications

\[1\] *Document similarity measures can support semi-automated identification of unreported links
between trial registrations and published reports.*  Adam G. Dunn, Enrico Coiera, Florence T. Bourgeois.
[*Submitted to the Journal of Clinical Epidemiology, 2017*] ArXiv version: https://arxiv.org/pdf/1709.02116.pdf
