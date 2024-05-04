from collections import OrderedDict
from datetime import datetime
from typing import List, Optional

from aiosumma import SummaClient

TEMPORAL_RANKING_FORMULA = "original_score * custom_score * fastsigm(abs(now - issued_at) / (86400 * 3) + 5, -1)"
PR_TEMPORAL_RANKING_FORMULA = f"{TEMPORAL_RANKING_FORMULA} * fastsigm(iqpr(quantized_page_rank), 0.15)"


default_field_aliases = {
    'ark_id': 'id.ark_ids',
    'ark_ids': 'id.ark_ids',
    'author': 'authors.family',
    'authors': 'authors.family',
    'cid': 'links.cid',
    'doi': 'id.dois',
    'ev': 'metadata.event.name',
    'extension': 'links.extension',
    'format': 'links.extension',
    'isbn': 'metadata.isbns',
    'isbns': 'metadata.isbns',
    'issn': 'metadata.issns',
    'issns': 'metadata.issns',
    'lang': 'languages',
    'magzdb_id': 'magzdb_id',
    'manualslib_id': 'id.manualslib_id',
    'nexus_id': 'id.nexus_id',
    'oclc_id': 'id.oclc_ids',
    'pmid': 'id.pubmed_id',
    'pub': 'metadata.publisher',
    'pubmed_id': 'id.pubmed_id',
    'rd': 'references.doi',
    'ser': 'metadata.series',
    'wiki': 'id.wiki',
}


default_term_field_mapper_configs = {
    'doi': {'fields': ['id.dois']},
    'doi_isbn': {'fields': ['metadata.isbns']},
    'isbn': {'fields': ['metadata.isbns']},
}


default_field_boosts = {
    'authors': 1.7,
    'content': 0.65,
    'extra': 1.7,
    'title': 1.85,
}


async def get_documents_on_topic(
    summa_client: SummaClient,
    topic: str,
    documents: int = 20,
    index_alias: str = 'stc',
    ranking_formula: Optional[str] = None,
    is_fieldnorms_scoring_enabled: bool = False,
    default_fields: List[str] = ("abstract", "title", "content"),
):
    return await summa_client.search_documents({
        "index_alias": index_alias,
        "query": {"boolean": {"subqueries": [{
            "occur": "should",
            "query": {
                "match": {
                    "value": topic,
                    "query_parser_config": {
                        "default_fields": list(default_fields),
                        "field_aliases": default_field_aliases,
                        "field_boosts": default_field_boosts,
                    },
                }
            },
        }]}},
        "collectors": [{"top_docs": {"limit": documents, "scorer": {
            "eval_expr": ranking_formula or PR_TEMPORAL_RANKING_FORMULA,
        }}}],
        "is_fieldnorms_scoring_enabled": is_fieldnorms_scoring_enabled,
    })


def get_full_query_parser_config(query_language: Optional[str] = None, exact_matches_promoter_slop: int = 4, exact_matches_promoter_boost: float = 2.0):
    query_parser_config = {
        'default_fields': ['abstract', 'concepts', 'content', 'extra', 'title'],
        'term_limit': 20,
        'field_aliases': default_field_aliases,
        'field_boosts': default_field_boosts,
        'exact_matches_promoter': {
            'slop': exact_matches_promoter_slop,
            'boost': exact_matches_promoter_boost,
            'fields': ['abstract', 'extra', 'title']
        }
    }
    if query_language:
        query_parser_config['query_language'] = query_language
    return query_parser_config


def get_light_query_parser_config(query_language: Optional[str] = None):
    query_parser_config = {
        'default_fields': ['abstract', 'title'],
        'term_limit': 20,
        'field_aliases': default_field_aliases,
        'field_boosts': default_field_boosts,
    }
    if query_language:
        query_parser_config['query_language'] = query_language
    return query_parser_config


def get_query_parser_config(profile: str, query_language: Optional[str] = None, exact_matches_promoter_boost: float = 2.0):
    if profile == 'full':
        return get_full_query_parser_config(query_language, exact_matches_promoter_boost)
    elif profile == 'light':
        return get_light_query_parser_config(query_language)
    else:
        raise ValueError("Unknown profile")


def get_default_scorer(profile: str):
    if profile == 'full':
        return {'eval_expr': PR_TEMPORAL_RANKING_FORMULA}
    elif profile == 'light':
        return None
    else:
        raise ValueError("Unknown profile")


def format_document(document: dict):
    parts = []
    if title := document.get('title'):
        parts.append(f'Title: {title}')
    if authors := document.get('authors'):
        parts.append(f'Authors: {authors}')
    if id_ := document.get('id'):
        parts.append(f'ID: {id_}')
    if links := document.get('links'):
        parts.append(f'Links: {links}')
    if abstract := document.get('abstract'):
        parts.append(f'Abstract: {abstract[:200]}')
    return '\n'.join(parts)


def plain_author(author):
    text = None
    if "family" in author and "given" in author:
        text = f"{author['given']} {author['family']}"
    elif "family" in author or "given" in author:
        text = author.get("family") or author.get("given")
    elif "name" in author:
        text = author["name"]
    return text


def generate_snippet(document: dict, content: str):
    snippet = {
        "snippet": content,
        "title": document["title"],
        "id": document["id"]["nexus_id"],
    }
    if document["issued_at"] != -62135596800:
        snippet["year"] = datetime.fromtimestamp(document["issued_at"], tz=None).year
    if container_title := document.get('metadata', {}).get('container_title'):
        snippet["journal_name"] = container_title
    if publisher := document.get('publisher', {}).get('publisher'):
        snippet["publisher"] = publisher
    if authors := document.get('authors'):
        snippet['authors'] = list(map(plain_author, authors[:3]))
    return snippet


class BaseDocumentHolder:
    def __init__(self, document):
        self.document = document

    def __getattr__(self, name):
        if name in self.document:
            return self.document[name]
        if name == 'content':
            return
        elif 'metadata' in self.document and name in self.document['metadata']:
            return self.document['metadata'][name]
        elif 'id' in self.document and name in self.document['id']:
            return self.document['id'][name]

    def has_cover(self):
        return bool(self.isbns and len(self.isbns) > 0)

    def get_links(self):
        if self.has_field('links') and self.links:
            return LinksWrapper(self.links)
        return LinksWrapper([])

    @property
    def ordered_links(self):
        links = self.get_links()
        pdf_link = None
        epub_link = None
        other_links = []
        for link in links.links.values():
            if link['extension'] == 'pdf' and not pdf_link:
                pdf_link = link
            elif link['extension'] == 'pdf' and not epub_link:
                epub_link = link
            else:
                other_links.append(link)
        if epub_link:
            other_links = [epub_link] + other_links
        if pdf_link:
            other_links = [pdf_link] + other_links
        return other_links

    @property
    def doi(self):
        if self.has_field('dois') and self.dois:
            return self.dois[0]

    def has_field(self, name):
        return (
            name in self.document
            or name in self.document.get('metadata', {})
            or name in self.document.get('id', {})
        )

    def get_external_id(self):
        if self.doi:
            return f'id.dois:{self.doi}'
        elif self.internal_iso:
            return f'id.internal_iso:{self.internal_iso}'
        elif self.internal_bs:
            return f'id.internal_bs:{self.internal_bs}'
        elif self.pubmed_id:
            return f'id.pubmed_id:{self.pubmed_id}'
        elif self.ark_ids:
            return f'id.ark_ids:{self.ark_ids[-1]}'
        elif self.libgen_ids:
            return f'id.libgen_ids:{self.libgen_ids[-1]}'
        elif self.zlibrary_ids:
            return f'id.zlibrary_ids:{self.zlibrary_ids[-1]}'
        elif self.wiki:
            return f'id.wiki:{self.wiki}'
        elif self.magzdb_id:
            return f'id.magzdb_id:{self.magzdb_id}'
        elif self.manualslib_id:
            return f'id.manualslib_id:{self.manualslib_id}'
        elif self.oclc_ids:
            return f'id.oclc_ids:{self.oclc_ids[-1]}'
        else:
            return None

    def get_id(self):
        if self.nexus_id:
            return f'id.nexus_id:{self.nexus_id}'
        else:
            return self.get_external_id()


class LinksWrapper:
    def __init__(self, links):
        self.links = OrderedDict()
        for link in links:
            self.add(link)

    def reset(self):
        self.links = OrderedDict()

    def to_list(self):
        return list(self.links.values())

    def add(self, link):
        old_link = self.links.pop(link['cid'], None)
        self.links[link['cid']] = link
        return old_link

    def prepend(self, link):
        old_link = self.add(link)
        self.links.move_to_end(link['cid'], False)
        return old_link

    def delete_links_with_extension(self, extension):
        for cid in list(self.links.keys()):
            if self.links[cid]['extension'] == extension:
                del self.links[cid]

    def override_link_with_extension(self, new_link):
        self.delete_links_with_extension(new_link['extension'])
        return self.prepend(new_link)

    def remove_cid(self, cid):
        return self.links.pop(cid, None)

    def get_link_with_extension(self, extension: Optional[str] = None, from_end: bool = False):
        return self.get_first_link(extension=extension, from_end=from_end)

    def get_first_link(self, extension: Optional[str] = None, from_end: bool = False):
        links = list(self.links.values())
        if from_end:
            links = reversed(links)
        for link in links:
            if extension is None or link['extension'] == extension:
                return link
