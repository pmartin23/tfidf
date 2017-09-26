from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy
import numpy as np
from scipy.sparse import csr_matrix
import pickle
import requests
import untangle
import json


def gen_tfidf_matrix(corpus, vectorizer_fname, matrix_fname):
    """
    generate and pickle a tfidf vectorizer & tfidf matrix for the given corpus of documents

    @param corpus: list of document strings
    @param vectorizer_fname: filename for tfidf vectorizer pickle
    @param matrix_fname: filename for tfidf matrix pickle
    @return: None
    """
    tfidf_vectorizer = TfidfVectorizer(use_idf=True)
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
    scipy.sparse.save_npz(matrix_fname + '.npz', tfidf_matrix)
    pickle.dump(tfidf_vectorizer, open(vectorizer_fname + '.pickle', 'wb'))


def docsim(document, tfidf_vectorizer, tfidf_matrix):
    """
    rank all documents in the given tfidf matrix accordinig to their similarity to input document

    @param document: input document text
    @param tfidf_vectorizer: tfidf vectorizer used to generate tfidf matrix
    @param tfidf_matrix: of tfidf scores for candidate documents and word features
    @return: ranked list of document indices according to similarity with input document
    """
    tf_transformer = TfidfVectorizer(use_idf=False)
    normalised_tf_vector = tf_transformer.fit_transform([document])
    idf_indices = [tfidf_vectorizer.vocabulary_[feature_name] for feature_name in tf_transformer.get_feature_names() if
                   feature_name in tfidf_vectorizer.vocabulary_.keys()]
    tf_indices = [tf_transformer.vocabulary_[feature_name] for feature_name in tfidf_vectorizer.get_feature_names() if
                  feature_name in tf_transformer.vocabulary_.keys()]
    final_idf = tfidf_vectorizer.idf_[np.array(idf_indices)]
    final_tf = np.array(normalised_tf_vector.toarray()[0])[np.array(tf_indices)]
    document_tfidf = np.asmatrix(final_tf * final_idf)
    tfidf_matrix = tfidf_matrix[:, np.array(idf_indices)]
    cos_sim = cosine_similarity(document_tfidf, tfidf_matrix).flatten()
    related_docs_indices = cos_sim.argsort()[::-1]
    return related_docs_indices


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


def _concat_dict_vals(dict):
    """
    concat all values in a dict into a single string

    @param dict: input dict
    @return: string of concatenated values
    """
    none_removed = (t for t in dict.values() if t is not None)
    document = """ """.join(none_removed)
    return document



