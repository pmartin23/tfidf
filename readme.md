# Document similarity measures using tfidf & cosine similarity

This script will rank candidate PubMed articles according to their similarity to a nominated ClinicalTrials.gov registry entry, using tfidf and cosine similarity.

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

Note for Microsoft Windows users: replace the virtual environment activation command above with tfidf_bot\Scripts\activate

## Example

Below is an example usage of the script that will output the ids of candidate PubMed articles in ranked order according to their similarity to the specified ClinicalTrials.gov registry entry

```
from tfidf import ctgov_text, pubmed_text, gen_tfidf_matrix, docsim

matrix_fname = 'pubmed_tfidf'
vectorizer_fname = 'pmid_vec'
nct_id = 'NCT03132233'
candidate_ids = np.array(['24601174', '19515181', '22512265'])

nct_doc = ctgov_text(nct_id)  # retrieve trial registry text
candidate_docs = [pubmed_text(pmid) for pmid in candidate_ids]  # retrieve text for candidate pubmed articles
gen_tfidf_matrix(candidate_docs, vectorizer_fname,
                 matrix_fname)  # generate tfidf matrix for candidate pubmed articles
tfidf_vectorizer = pickle.load(open(vectorizer_fname + ".pickle"))  # load tfidf vectorizer
tfidf_matrix = scipy.sparse.load_npz(matrix_fname + '.npz')  # load tfidf matrix
ranks = docsim(nct_doc, tfidf_vectorizer, tfidf_matrix)  # calculate the rank of each candidate document
print candidate_ids[ranks]
```

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