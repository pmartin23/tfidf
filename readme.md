# Document similarity measures using tfidf & cosine similarity

This script will rank candidate PubMed articles according to the cosine similarity to a nominated ClinicalTrials.gov.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Requirements

To install and run this example, you will need:
 
 * Git
 * Python 2.7 
 * and virtualenv (which you can install easily using [pip](https://pypi.python.org/pypi/pip))

### Installing

Run the comamnds below to set everything up such that you will be able to run the script with your own input

```
$ git clone https://git.aihi.mq.edu.au/paige_newman/tfidf_bot.git tfidf_bot
$ virtualenv tfidf_bot
$ tfidf_bot/bin/activate
(tfidf_bot) cd tfidf_bot
(tfidf_bot) pip install -r requirements.txt
```
Note for Microsoft Windows users: replace the virtual environment activation command above with ```tfidf_bot\Scripts\activate```

## Example

First, generate and save the tfidf matrix and vectorizer model for the corups of candidate PubMed articles. In this example,
 our features are the terms in the title and abstract of each PubMed article. It may take a while to retrieve all article 
 title & abstract metadata and construct the matrix.
```
from tfidf import ctgov_text, pubmed_text, gen_tfidf_matrix, docsim

matrix_fname = 'pubmed_tfidf'
vectorizer_fname = 'pmid_vec'
candidate_ids = np.array(['24601174', '19515181', '22512265'])
candidate_docs = [pubmed_text(pmid) for pmid in candidate_ids]  # retrieve text for candidate pubmed articles
gen_tfidf_matrix(candidate_docs, vectorizer_fname, matrix_fname)

```

Next, we will nominate a registry entry, and call the ```docsim ``` method, which will:
 * Calculate the tfidf of the registry entry with respect to the features in the corpus of candidate PubMed articles. In this example, we used all terms within the fields 'brief title', 'official title', 'brief summary', 'detailed description', 
and 'condition' of the registry entry metadata, as features.

* Produce a rank for each PubMed article according to its similarity with the registry entry. The similarity is 
determined by calculating the cosine similarity between the vector representing the tfidf of each candidate PubMed article,
and the vector representing the tfidf of the registry entry.

```
nct_id = 'NCT03132233'
nct_doc = ctgov_text(nct_id)
tfidf_vectorizer = pickle.load(open(vectorizer_fname + ".pickle"))  
tfidf_matrix = scipy.sparse.load_npz(matrix_fname + '.npz') 
ranks = docsim(nct_doc, tfidf_vectorizer, tfidf_matrix)
```
We can then see the resulting ranks 

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc