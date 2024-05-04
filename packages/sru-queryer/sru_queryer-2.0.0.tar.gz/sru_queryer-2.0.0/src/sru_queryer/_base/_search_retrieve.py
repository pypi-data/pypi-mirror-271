from __future__ import annotations
from requests import Request

from ._search_clause import SearchClause
from ._raw_cql import RawCQL
from ._cql_boolean_operators import CQLBooleanOperatorBase
from ._sru_configuration import SRUConfiguration
from ._sru_validator import SRUValidator
from ._sru_aux_formatter import SRUAuxiliaryFormatter
from ._sort_key import SortKey

class SearchRetrieve:

    def __init__(self, sru_configuration: SRUConfiguration, cql_query: SearchClause | CQLBooleanOperatorBase | RawCQL, start_record: int | None = None, maximum_records: int | None = None, record_schema: str | None = None, sort_queries: list[dict] | list[SortKey] | None = None, record_packing: str | None = None):
        self.sru_configuration = sru_configuration
        self.cql_query = cql_query
        self.start_record = start_record
        self.maximum_records = maximum_records
        self.record_schema = record_schema
        self.record_packing = record_packing

        if sru_configuration.sru_version == "1.2":
            if sort_queries and isinstance(sort_queries[0], SortKey):
                raise ValueError("You cannot use SortKeys with SRU version 1.2. Please see documentation on constructing a SortBy request.")
        if sru_configuration.sru_version == "1.1":
            if sort_queries and not isinstance(sort_queries[0], SortKey):
                raise ValueError("You must use SortKeys for sorting with SRU version 1.1. Please see documentation on SortKey objects.")
        self.sort_queries = sort_queries

    def validate(self):
        """Validates the searchRetrieve request. 
        Keep in mind that not all facets of the request are validated."""

        SRUValidator.validate_defaults(self.sru_configuration)

        SRUValidator.validate_base_query(self.sru_configuration,
            self.start_record, self.maximum_records, self.record_schema, self.record_packing)

        self.cql_query.validate(self.sru_configuration)

        SRUValidator.validate_sort(self.sru_configuration, self.sort_queries, self.record_schema)

    def construct_request(self) -> Request:
        """Constructs the searchRetrieve request.

        Constructs the searchRetrieve request, including the base request, CQL query, and sortBy.

        If you added a username and password when initializing SRUQueryer, it will be added to the
        headers of the request using the 'Basic access authentication' protocol.

        Returns a Request object. You can execute it using an instance of requests.Session:\n
            request = request.prepare()\n
            s = requests.Session()\n
            response = s.send(request)\n"""
        search_retrieve_query = SRUAuxiliaryFormatter.format_base_search_retrieve_query(self.sru_configuration,
            self.start_record, self.maximum_records, self.record_schema, self.record_packing)

        # if isinstance(self.cql_query, SearchClause) and not (self.cql_query.get_index_name() and self.cql_query.get_relation()):
        #     # If it's just a single value (search term) as the query, without anything else, append an equals sign.
        #     search_retrieve_query += "="
        # This ^ caused the query to fail. I'm not sure why I put it here, but I'm leaving it here just in case.
        search_retrieve_query += self.cql_query.format()

        search_retrieve_query += SRUAuxiliaryFormatter.format_sort_query(self.sort_queries)

        # Create the actual request object
        request = Request("GET", search_retrieve_query)
        if self.sru_configuration.username and self.sru_configuration.password:
            request.headers["Authorization"] = SRUAuxiliaryFormatter.format_basic_access_authentication_header_payload(self.sru_configuration.username, self.sru_configuration.password)

        return request
