from bson import ObjectId
from typing import Literal
from dataclasses import dataclass


@dataclass(slots=True)
class Keyword:
    word: str
    score: int


@dataclass(slots=True)
class CompanyKeywords:
    _id: ObjectId
    company_id: str # _id filed from a Company
    keywords: list[Keyword]
    language: Literal["fr", "en", "nl"]


def convert_dict_to_keyword_list(company_keywords_dict: dict) -> CompanyKeywords:
    """
    Convert a dict to a CompanyKeywords object.

    :param company_keywords_dict: The dict to convert.
    :return: A CompanyKeywords object.
    """
    keywords = [Keyword(**keyword) for keyword in company_keywords_dict['keywords']]
    return CompanyKeywords(
        _id=company_keywords_dict['_id'],
        company_id=company_keywords_dict['company_id'],
        language=company_keywords_dict['language'],
        keywords=keywords
    )
