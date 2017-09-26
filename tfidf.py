from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy
import numpy as np
from scipy.sparse import csr_matrix
import pickle


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







