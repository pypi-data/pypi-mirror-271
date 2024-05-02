import sqlite3
import os
from typing import List, Union, Iterator
from contextlib import contextmanager
from .stopwords import stopwords

_DB_FILE = "{}/cim-11.sqlite3".format(os.path.dirname(__file__))


@contextmanager
def _db_cursor():
    db = sqlite3.connect(f"file:{_DB_FILE}?mode=ro", uri=True)
    cursor = db.cursor()
    yield cursor
    db.close()


class Concept:
    def __init__(
        self,
        idc_id: str,
        icode: str = None,
        label: str = None,
        parent_idc_id: str = None,
        label_en: str = None,
    ):
        self.idc_id = idc_id
        self.icode = icode
        self.label = label
        self.parent_idc_id = parent_idc_id
        self.label_en = label_en

    @property
    def children(self) -> List["Concept"]:
        items = []
        with _db_cursor() as cursor:
            for row in cursor.execute(
                "SELECT idc_id, icode, label, parent_idc_id, label_en from cim11 where parent_idc_id = ?",
                (self.idc_id,),
            ):
                items.append(Concept(row[0], row[1], row[2], row[3], row[4]))
        return items

    @property
    def parent(self) -> Union["Concept", None]:
        with _db_cursor() as cursor:
            for row in cursor.execute(
                "SELECT idc_id, icode, label, parent_idc_id, label_en from cim11 where idc_id = ?",
                (self.parent_idc_id,),
            ):
                return Concept(row[0], row[1], row[2], row[3], row[4])

    def __str__(self):
        if self.icode:
            return f"{self.icode} {self.label}"
        else:
            return ""


def all_concepts() -> Iterator[Concept]:
    with _db_cursor() as cursor:
        for row in cursor.execute(
            "SELECT idc_id, icode, label, parent_idc_id, label_en from cim11"
        ):
            yield Concept(row[0], row[1], row[2], row[3], row[4])


def root_concepts() -> List[Concept]:
    """
    Fetches the root concepts from the database.

    :return: A list of Concept objects representing the root concepts.
    """
    items = []
    with _db_cursor() as cursor:
        for row in cursor.execute(
            "SELECT idc_id, icode, label, parent_idc_id, label_en from cim11 where parent_idc_id is null"
        ):
            items.append(Concept(row[0], row[1], row[2], row[3], row[4]))
        return items


def autocomplete_label(terms: str, lang="fr") -> List[Concept]:
    """
    Returns a list of concepts that match the given terms.

    :param terms: The search terms to match against the concept labels.
    :type terms: str
    :return: A list of concepts that match the given terms.
    :rtype: List[Concept]
    """
    q = "SELECT idc_id, icode, label, parent_idc_id, label_en from cim11 where label like ? order by label"
    if lang == "en":
        q = "SELECT idc_id, icode, label, parent_idc_id, label_en from cim11 where label_en like ? order by label"
    items = []
    with _db_cursor() as cursor:
        for row in cursor.execute(
            q,
            (f"%{terms.strip()}%",),
        ):
            items.append(Concept(row[0], row[1], row[2], row[3], row[4]))
    return items


def filter_stopwords(terms: str, lang="fr") -> List[str]:
    wrds = []
    for wrd in terms.replace("'", " ").replace("’", " ").split(" "):
        if wrd not in stopwords.get(lang, []):
            wrds.append('"' + wrd.replace('"', '""') + '"')
    return wrds


def label_search(
    terms: str, lang="fr", search_type: str = "AND", filter_stopwords=False
) -> List[Concept]:
    """
    Search for concepts based on given terms.

    :param terms: The terms to search for.
    :param lang: iso-639-1 language. Can be "fr" or "en". Defaults to "fr".
    :param search_type: Can be "AND" or "OR". Defaults to "AND".
    :param filter_stopwords: Filter selected language stopwords. Defaults to False.
    :return: A list of concepts matching the search terms.
    """
    if search_type == "OR":
        search_type = " OR "
    else:
        search_type = " "

    def fts_escape(user_input: str) -> str:
        wrds = []
        for wrd in user_input.replace("'", " ").replace("’", " ").split(" "):
            if not filter_stopwords or (
                filter_stopwords and wrd not in stopwords.get(lang, [])
            ):
                wrds.append('"' + wrd.replace('"', '""') + '"')
        return search_type.join(wrds)

    dedup = []
    terms = fts_escape(terms)
    items = []
    q = "SELECT idc_id, icode, label, parent_idc_id, label_en from cim11 where label match ? and icode is not null order by icode"
    if lang == "en":
        q = "SELECT idc_id, icode, label, parent_idc_id, label_en from cim11 where label_en match ? and icode is not null order by icode"
    with _db_cursor() as cursor:
        for row in cursor.execute(
            q,
            (terms,),
        ):
            if row[1] not in dedup:
                items.append(Concept(row[0], row[1], row[2], row[3], row[4]))
                dedup.append(row[1])
    return items


def icode_search(code: str, partial=True) -> List[Concept]:
    """
    Searches for concepts in the database based on the provided code.

    :param code: The code to search for concepts with.
    :param partial: Set to True to search for concepts with codes starting with the provided code. Set to False to search for concepts with exact codes.
    :return: A list of Concept objects that match the search criteria.
    """
    items = []
    dedup = []
    partial_suffix = "%" if partial else ""
    with _db_cursor() as cursor:
        for row in cursor.execute(
            "SELECT idc_id, icode, label, parent_idc_id, label_en from cim11 where icode like ? order by icode",
            (f"{code}{partial_suffix}",),
        ):
            if row[1] not in dedup:
                items.append(Concept(row[0], row[1], row[2], row[3], row[4]))
                dedup.append(row[1])
    return items


def icode_details(complete_code: str) -> Union[Concept, None]:
    """
    Retrieve the details of a concept using its complete code.

    :param complete_code: The complete code of the concept.
    :return: The Concept object corresponding to the complete code, or None if not found.
    """
    with _db_cursor() as cursor:
        for row in cursor.execute(
            "SELECT idc_id, icode, label, parent_idc_id, label_en from cim11 where icode = ?",
            (complete_code,),
        ):
            return Concept(row[0], row[1], row[2], row[3], row[4])


def update_db(tabbed_file_path: str):
    import csv

    headers = []

    def depth_from_title(title: str) -> int:
        depth = 0
        offset = 0
        t_len = len(title)
        while offset < t_len:
            if title[offset : offset + 2] == "- ":
                depth = depth + 1
                offset = offset + 2
            else:
                break
        return depth

    with open(tabbed_file_path, "r") as f:
        db = sqlite3.connect(_DB_FILE)
        cursor = db.cursor()
        cursor.execute("delete from cim11")
        reader = csv.reader(f, dialect="excel-tab")
        data_path = []
        prev_data = {}
        parent = None
        for row in reader:
            if not headers:
                headers = row
                headers[0] = "Foundation URI"
            else:
                data = dict(zip(headers, row))
                data["depth"] = depth_from_title(data["TitleEN"])
                data["title_fr"] = data["Title"].lstrip("- ")
                data["title_en"] = data["TitleEN"].lstrip("- ")
                data["Foundation URI"] = (
                    None if data["Foundation URI"] == "" else data["Foundation URI"]
                )
                data["Linearization URI"] = (
                    None
                    if data["Linearization URI"] == ""
                    else data["Linearization URI"]
                )
                if prev_data and prev_data["depth"] != data["depth"]:
                    if prev_data and data["depth"] > prev_data["depth"]:
                        data_path.append(prev_data)
                        parent = data_path[-1]
                    if prev_data and data["depth"] < prev_data["depth"]:
                        data_path = data_path[0 : data["depth"]]
                        if len(data_path) > 0:
                            parent = data_path[-1]
                        else:
                            parent = None
                if parent and not data["Foundation URI"]:
                    adjective = data["Linearization URI"].split("/")[-1]
                    data["Foundation URI"] = (
                        parent["Foundation URI"] + "/mms/" + adjective
                    )
                cursor.execute(
                    "insert into cim11(idc_id, icode, label, parent_idc_id, label_en) VALUES (?,?,?,?,?)",
                    (
                        data["Foundation URI"],
                        data["Code"],
                        data["title_fr"],
                        parent["Foundation URI"] if parent else None,
                        data["title_en"],
                    ),
                )
                prev_data = data
        db.commit()
        db.close()
