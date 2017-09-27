from tfidf import gen_tfidf_matrix, docsim
import requests
import untangle
import json
import pickle
import scipy
from scipy.sparse import csr_matrix
import numpy as np

def _concat_dict_vals(dict):
    """
    concat all values in a dict into a single string

    @param dict: input dict
    @return: string of concatenated values
    """
    none_removed = (t for t in dict.values() if t is not None)
    document = """ """.join(none_removed)
    return document


def pubmed_text(pmid):
    """
       retrieve & concatenate article title & abstract from Pubmed, given PMID

       @param pmid: id of Pubmed article
       @type pmid: str
       @return: article metadata
       @rtype: dict
       """
    base_url_abs = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
    base_url_summary = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'
    result = {}
    abs = ""
    r = requests.get(base_url_abs,
                     params={'db': 'pubmed', 'id': pmid, 'retmode': 'XML', 'rettype': 'abstract'})
    obj = untangle.parse(r.content)
    if not hasattr(obj.PubmedArticleSet, 'PubmedArticle'):
        return False
    if hasattr(obj.PubmedArticleSet.PubmedArticle.MedlineCitation.Article, 'Abstract'):
        for child in obj.PubmedArticleSet.PubmedArticle.MedlineCitation.Article.Abstract.AbstractText:
            if child['Label']:
                abs += child['Label'] + ': '
            abs += child.cdata + ' '
        result["abstract"] = abs
    s = requests.get(base_url_summary, params={'db': 'pubmed', 'id': pmid, 'retmode': 'json'})
    s = json.loads(s.text)
    if 'result' in s:
        result["title"] = s['result'][str(pmid)]['title']
    document = _concat_dict_vals(result)
    return document


def ctgov_text(nct_id):
    """
    retrieve record from ClinicalTrials.gov, concatenate the fields 'condition', 'brief title', 'official title'
    'brief summary' and 'detailed description', return the resulting string

    @param nct_id: id of desired registry entry
    @return: concatenated field text
    """

    base_url = "https://clinicaltrials.gov/show/"
    url = base_url + nct_id
    r = requests.get(url, params={'displayxml': 'true'})
    try:
        obj = untangle.parse(r.content)
    except Exception:
        return False
    result = {'condition': '', 'detailed_description': ''}
    result['brief_title'] = obj.clinical_study.brief_title.cdata
    result['official_title'] = obj.clinical_study.official_title.cdata
    result['brief_summary'] = obj.clinical_study.brief_summary.textblock.cdata
    if hasattr(obj.clinical_study, 'detailed_description'):
        for desc in obj.clinical_study.detailed_description:
            result['detailed_description'] += desc.cdata
    if hasattr(obj.clinical_study, 'condition'):
        for condition in obj.clinical_study.condition:
            result['condition'] += ' ' + condition.cdata
    document = _concat_dict_vals(result)
    return document



if __name__ == "__main__":

    matrix_fname = 'pubmed_tfidf_example'
    vectorizer_fname = 'pubmed_vec_example'
    candidate_ids = np.array(['24601174', '19515181', '22512265'])
    candidate_docs = [pubmed_text(pmid) for pmid in candidate_ids]  # retrieve text for candidate pubmed articles
    gen_tfidf_matrix(candidate_docs, vectorizer_fname, matrix_fname)  # generate tfidf matrix for candidate pubmed articles


    nct_id = 'NCT03132233'
    nct_doc = ctgov_text(nct_id)  # retrieve trial registry text
    tfidf_vectorizer = pickle.load(open(vectorizer_fname + ".pickle"))  # load tfidf vectorizer
    tfidf_matrix = scipy.sparse.load_npz(matrix_fname + '.npz')  # load tfidf matrix
    ranks = docsim(nct_doc, tfidf_vectorizer, tfidf_matrix)  # calculate the rank of each candidate document
    ranked_pmids = candidate_ids[ranks]
    print ranked_pmids
