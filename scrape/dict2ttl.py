from rdflib import Graph, Literal, RDF, URIRef, Namespace, RDFS
from rdflib.collection import Collection
from rdflib.namespace import XSD
import urllib.parse
import pandas as pd

from rdflib import BNode


def add_to_graph(g, subject, predicate, object_, datatype=None, to_literal=True):
    """
    Add a triple to the RDF graph.

    Parameters
    ----------
    g : rdflib.Graph
        The RDF graph.
    subject : rdflib.URIRef or rdflib.BNode
        The subject of the triple.
    predicate : rdflib.URIRef
        The predicate of the triple.
    object_ : rdflib.URIRef or rdflib.BNode or rdflib.Literal or str or int
        The object of the triple.
    datatype : Optional[str]
        The datatype of the object if the object is to be added as a literal.
    to_literal : Optional[bool]
        Indicates if the object should be added as a literal or not. Default is True.
    Returns
    -------
    None
    """
    if object_ is not None:
        if to_literal:
            assert datatype is not None
            g.add((subject, predicate, Literal(object_, datatype=datatype)))
        else:
            g.add((subject, predicate, object_))


def convert_dict_to_graph(article_data):
    """
    Convert a dictionary containing information about an article to a RDF graph.

    Parameters
    ----------
    article_data : dict
        A dictionary containing various information about an article, such as the title, author,
        and publication date.

    Returns
    -------
    rdflib.graph.Graph
        A RDF graph representing the information in the input dictionary.
    """
    g = Graph()
    schema = Namespace('http://schema.org/')
    DC = Namespace('http://purl.org/dc/terms/')
    makg = Namespace('https://makg.org/class/')
    makg_property = Namespace('https://makg.org/property/')
    bn = Namespace('https://w3id.org/ocs/ont/papers/')
    datacite = Namespace('http://purl.org/spar/datacite/')
    fabio = Namespace('http://purl.org/spar/fabio/')
    g.bind("", bn)
    g.bind("makg_property", makg_property)
    g.bind("schema", schema)
    g.bind("dc", DC)
    g.bind("datacite", datacite)
    g.bind("fabio", fabio)
    g.bind("makg", makg)

    paper = Literal(article_data['title'])
    paper = URIRef(bn.paper)

    add_to_graph(g, makg.Author, RDFS.label, Literal('Author', lang="en"), to_literal=False)
    authors = BNode()

    authors_processed = []
    for i, author in enumerate(article_data['author']):
        author_ = URIRef(bn + f'author_{i}')
        add_to_graph(g, author_, RDF.type, makg.Author, to_literal=False)

        add_to_graph(g, author_, schema.name, author['given'], datatype=XSD.string)
        add_to_graph(g, author_, schema.familyName, author['family'], datatype=XSD.string)
        add_to_graph(g, authors, bn.hasItem, author_, to_literal=False)

        authors_processed.append(author_)

    add_to_graph(g, paper, DC.creator, authors, to_literal=False)

    add_to_graph(g, makg.Paper, RDFS.label, Literal('Paper', lang="en"), to_literal=False)
    add_to_graph(g, makg.Journal, RDFS.label, Literal('Journal', lang="en"), to_literal=False)

    add_to_graph(g, bn.journal, RDF.type, makg.Journal, to_literal=False)

    add_to_graph(g, bn.journal, schema.WebSite, article_data['volume_url'], datatype=XSD.anyURI)

    add_to_graph(g, bn.journal, schema.name, article_data['journal_name'], datatype=XSD.string)

    add_to_graph(g, paper, makg_property.appearsInJournal, bn.journal, to_literal=False)

    add_to_graph(g, makg.ConferenceInstance, RDFS.label, Literal('Conference', lang="en"), to_literal=False)

    add_to_graph(g, bn.conference, RDF.type, makg.ConferenceInstance, to_literal=False)
    add_to_graph(g, bn.conference, schema.name, article_data['session'], datatype=XSD.string)
    add_to_graph(g, paper, makg_property.appearsInConferenceInstance, bn.conference, to_literal=False)

    add_to_graph(g, paper, RDF.type, makg.Paper, to_literal=False)
    add_to_graph(g, paper, DC.title, article_data['title'], datatype=XSD.string)
    add_to_graph(g, paper, schema.url, article_data['url'], datatype=XSD.anyURI)

    add_to_graph(g, paper, schema.datePublished, article_data['date'], datatype=XSD.date)

    add_to_graph(g, paper, schema.numberOfPages, article_data['pages'], datatype=XSD.integer)

    add_to_graph(g, paper, DC.publisher, article_data['publisher'], datatype=XSD.string)

    add_to_graph(g, paper, DC.abstract, article_data['abstract'], datatype=XSD.string)

    add_to_graph(g, paper, DC.language, article_data['language'], datatype=XSD.string)

    add_to_graph(g, paper, DC.licence, article_data['licence'], datatype=XSD.anyURI)
    add_to_graph(g, paper, schema.additionalType, article_data['type'], datatype=XSD.string)

    add_to_graph(g, paper, DC.source, article_data['source'], datatype=XSD.string)

    add_to_graph(g, paper, datacite.issn, article_data['ISSN'], datatype=XSD.string)

    add_to_graph(g, paper, datacite.issn, article_data['ISSN'], datatype=XSD.string)

    add_to_graph(g, paper, datacite.doi, article_data['DOI'], datatype=XSD.string)
    return g.serialize(format='turtle')
