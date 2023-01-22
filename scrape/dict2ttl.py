from rdflib import Graph, Literal, RDF, URIRef, Namespace, RDFS
from rdflib.collection import Collection
from rdflib.namespace import XSD
import urllib.parse
import pandas as pd

from rdflib import BNode


def add_to_graph(g, subject, predicate, object_):
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
    object_ : rdflib.URIRef or rdflib.BNode or rdflib.Literal
        The object of the triple.

    Returns
    -------
    None
    """
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
    g.bind("schema", schema)
    g.bind("dc", DC)
    g.bind("datacite", datacite)
    g.bind("fabio", fabio)
    g.bind("makg", makg)

    paper = Literal(article_data['title'])  # .replace(' ', '_').replace(':', '_'))
    paper = URIRef(bn.paper)

    add_to_graph(g, makg.Author, RDFS.label, Literal('Author', lang="en"))
    authors = BNode()

    authors_processed = []
    for i, author in enumerate(article_data['author']):
        author_ = URIRef(bn + f'author_{i}')
        add_to_graph(g, author_, RDF.type, makg.Author)
        add_to_graph(g, author_, schema.name, Literal(author['given'], datatype=XSD.string))
        add_to_graph(g, author_, schema.familyName, Literal(author['family'], datatype=XSD.string))
        add_to_graph(g, authors, schema.hasItem, author_)
        authors_processed.append(author_)

    add_to_graph(g, paper, DC.creator, authors)

    add_to_graph(g, makg.Paper, RDFS.label, Literal('Paper', lang="en"))
    add_to_graph(g, makg.Journal, RDFS.label, Literal('Journal', lang="en"))

    add_to_graph(g, bn.journal, RDF.type, makg.Journal)
    add_to_graph(g, bn.journal, schema.WebSite, Literal(article_data['volume_url'], datatype=XSD.anyURI))
    add_to_graph(g, bn.journal, schema.name, Literal(article_data['journal_name'], datatype=XSD.string))

    add_to_graph(g, paper, makg.appearsInJournal, bn.journal)

    add_to_graph(g, makg_property.ConferenceInstance, RDFS.label, Literal('Conference', lang="en"))

    add_to_graph(g, bn.conference, RDF.type, makg.ConferenceInstance)
    add_to_graph(g, bn.conference, schema.name, Literal(article_data['session'], datatype=XSD.string))
    add_to_graph(g, paper, makg_property.appearsInConferenceInstance, bn.conference)

    add_to_graph(g, paper, RDF.type, makg.Paper)
    add_to_graph(g, paper, DC.title, Literal(article_data['title'], datatype=XSD.anyURI))
    add_to_graph(g, paper, schema.url, Literal(article_data['url'], datatype=XSD.anyURI))

    add_to_graph(g, paper, schema.datePublished, Literal(article_data['date'], datatype=XSD.date))

    add_to_graph(g, paper, schema.numberOfPages, Literal(article_data['pages'], datatype=XSD.integer))

    add_to_graph(g, paper, DC.publisher, Literal(article_data['publisher'], datatype=XSD.string))

    add_to_graph(g, paper, DC.abstract, Literal(article_data['abstract'], datatype=XSD.string))

    add_to_graph(g, paper, DC.language, Literal(article_data['language'], datatype=XSD.string))
    add_to_graph(g, paper, DC.licence, Literal(article_data['licence'], datatype=XSD.anyURI))

    add_to_graph(g, paper, schema.additionalType, Literal(article_data['type'], datatype=XSD.string))

    add_to_graph(g, paper, DC.source, Literal(article_data['source'], datatype=XSD.string))

    add_to_graph(g, paper, datacite.issn, Literal(article_data['ISSN'], datatype=XSD.string))

    add_to_graph(g, paper, datacite.doi, Literal(article_data['DOI'], datatype=XSD.string))

    add_to_graph(g, paper, fabio.hasDiscipline, Literal(None, datatype=XSD.string))

    return g.serialize(format='turtle')
