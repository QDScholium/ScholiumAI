import re
from typing import Optional
import requests

class BaseOpenAlexHandler:
    """
    Abstract base class for handling OpenAlex API requests and responses.
    Provides a standardized interface for making requests to the OpenAlex API,
    translating requests into the appropriate format, and processing responses.
    """   
    def __init__(self, email:str, api_key: Optional[str] = None):
        """Initialize the OpenAlex handler."""
        self.headers = {}
        self.params = {}
        if email:
            # Validate email format
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                raise ValueError(f"Invalid email format: {email}")
            
            self.headers["User-Agent"] = f"mailto:{email}"

        if api_key:
            self.params["api_key"] = api_key
        
        self.base_url = "https://api.openalex.org/"

    def make_request(
        self, 
        endpoint: str, 
        params: dict = None
    ):
        """
        Make a request to the OpenAlex API.
        """
        params = {**params, **self.params}
        url = self.base_url + endpoint
        response = requests.get(url=url, params=params, headers=self.headers)
        return response.json()
    
    def translate_request(self, query: str, filters: dict = None, n_results: Optional[int] = None):
        """
        Translate a natural language query and filters into OpenAlex API parameters.
        
        Args:
            query (str): The search query.
            filters (dict, optional): Additional filters to apply to the search.
            n_results (int, optional): Number of results to return.
            
        Returns:
            dict: Parameters formatted for the OpenAlex API
        """
        params = {"search": query}
        
        if filters:
            for key, value in filters.items():
                params[key] = value
                
        if n_results:
            params["per_page"] = n_results
            
        return params
    
    def translate_response(self, raw_response):
        """
        Process and transform the OpenAlex API response into a standardized format.
        
        Args:
            raw_response (dict): The raw response from the OpenAlex API.
            
        Returns:
            list: A list of standardized institution objects extracted from the response.
        """
        return raw_response["results"]
    
    def search(self, query: str, endpoint: str, filters: dict = None, n_results: Optional[int] = None, **kwargs):
        """
        Searches the OpenAlex API for topics with the given query and filters.
        
        Args:
            query (str): The search query string
            filters (dict, optional): Dictionary of filters to apply to the search
            n_results (int, optional): Number of results to return
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: The search results from the OpenAlex API
        """
        params = self.translate_request(query, filters=filters, n_results=n_results)
        if kwargs:
            params.update(kwargs)
        raw_response = self.make_request(endpoint, params)
        return self.translate_response(raw_response=raw_response)
    

class WorksHandler(BaseOpenAlexHandler):
    def __init__(
        self, 
        email: str, 
        api_key: Optional[str] = None
    ):
        self.supported_filters = {
            "authorships.affiliations.institution_ids",
            "authorships.author.id",
            "author.id",
            "authorships.author.orcid",
            "authorships.countries",
            "authorships.institutions.country_code",
            "authorships.institutions.id",
            "authorships.institutions.lineage",
            "authorships.institutions.ror",
            "authorships.institutions.type",
            "authorships.is_corresponding",
            "apc_list.value",
            "apc_list.currency",
            "apc_list.provenance",
            "apc_list.value_usd",
            "apc_paid.value",
            "apc_paid.currency",
            "apc_paid.provenance",
            "apc_paid.value_usd",
            "best_oa_location.is_accepted",
            "best_oa_location.is_published",
            "best_oa_location.license",
            "best_oa_location.source.id",
            "best_oa_location.source.is_in_doaj",
            "best_oa_location.source.issn",
            "best_oa_location.source.host_organization",
            "best_oa_location.source.type",
            "best_oa_location.version",
            "biblio.first_page",
            "biblio.issue",
            "biblio.last_page",
            "biblio.volume",
            "cited_by_count",
            "concepts.id",
            "concepts.wikidata",
            "corresponding_author_ids",
            "corresponding_institution_ids",
            "countries_distinct_count",
            "doi",
            "fulltext_origin",
            "fwci",
            "grants.award_id",
            "grants.funder",
            "has_fulltext",
            "ids.pmcid",
            "ids.pmid",
            "ids.openalex",
            "ids.mag",
            "indexed_in",
            "institutions_distinct_count",
            "is_paratext",
            "is_retracted",
            "keywords.keyword",
            "language",
            "locations.is_accepted",
            "locations.is_oa",
            "locations.is_published",
            "locations.license",
            "locations.source.id",
            "locations.source.is_core",
            "locations.source.is_in_doaj",
            "locations.source.issn",
            "locations.source.host_organization",
            "locations.source.type",
            "locations.version",
            "locations_count",
            "open_access.any_repository_has_fulltext",
            "open_access.is_oa",
            "open_access.oa_status",
            "primary_location.is_accepted",
            "primary_location.is_oa",
            "primary_location.is_published",
            "primary_location.license",
            "primary_location.source.id",
            "primary_location.source.is_core",
            "primary_location.source.is_in_doaj",
            "primary_location.source.issn",
            "primary_location.source.host_organization",
            "primary_location.source.type",
            "primary_location.version",
            "primary_topic.id",
            "primary_topic.domain.id",
            "primary_topic.field.id",
            "primary_topic.subfield.id",
            "publication_year",
            "publication_date",
            "sustainable_development_goals.id",
            "topics.id",
            "topics.domain.id",
            "topics.field.id",
            "topics.subfield.id",
            "type",
            "type_crossref"
        }
        self.search_fields = {
            "abstract.search",
            "display_name.search",
            "fulltext.search",
            "raw_affiliation_strings.search",
            "title.search",
            "title_and_abstract.search",
            "default.search"
        }
        super().__init__(email, api_key)
    
    def translate_request(
        self, 
        query: str,
        filters: dict = None, 
        n_results: Optional[int] = None
    ) -> dict:
        """
        Translates a query and filters into a format suitable for OpenAlex API.
        
        Args:
            query (str): The search query string
            filters (dict, optional): Dictionary of filters to apply to the search
            
        Returns:
            dict: A dictionary containing the translated request parameters
        """
        params = {}
        
        query = query.strip()
        params["search"] = query
        
        if filters and isinstance(filters, dict):
            filter_params = []
            
            for key, value in filters.items():
                if key in self.supported_filters and value is not None:
                    if isinstance(value, list):
                        filter_params.append(f"{key}:{"|".join(str(v) for v in value)}")
                    else:
                        filter_params.append(f"{key}:{value}")
            
            if filter_params:
                params["filter"] = ",".join(filter_params)
        
        if n_results:
            params["sample"] = n_results
        
        return params
    
    def make_request(
        self, 
        endpoint: str, 
        params: dict = None
    ):
        """
        Make a request to the OpenAlex API.
        
        Args:
            endpoint (str): The API endpoint to request (e.g., 'works', 'authors').
            params (dict, optional): Query parameters for the request.
            
        Returns:
            dict: The JSON response from the API parsed as a dictionary.
            
        Example:
            >>> response = handler.make_request('works', {'search': 'machine learning'})
        """
        params = {**params, **self.params}
        url = self.base_url + endpoint
        response = requests.get(url=url, params=params, headers=self.headers)
        return response.json()

    def translate_response(self, raw_response):
        """
        Process and transform the OpenAlex API response into a standardized format.
        
        Args:
            response (dict): The raw response from the OpenAlex API.
            
        Returns:
            list: A list of standardized work objects extracted from the response.
        """
        return raw_response["results"]       

    def search(
        self, 
        query: str, 
        filters: dict = None, 
        n_results: Optional[int] = None, 
        **kwargs
    ):
        """
        Searches the OpenAlex API with the given query and filters.
        
        Args:
            query (str): The search query string
            filters (dict, optional): Dictionary of filters to apply to the search
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            dict: The search results from the OpenAlex API
        """
        params = self.translate_request(query, filters=filters, n_results=n_results)
        if kwargs:
            params.update(kwargs)
        endpoint = "works"  
        raw_response = self.make_request(endpoint, params)
        return self.translate_response(raw_response=raw_response)

class AuthorHandler(BaseOpenAlexHandler):
    """
    Handler for the OpenAlex Authors API endpoint.
    
    This class provides methods to search for authors and process author data
    from the OpenAlex API.
    """
    
    def search(self, query: str, filters: dict = None, n_results: Optional[int] = None, **kwargs):
        """
        Searches the OpenAlex API for authors with the given query and filters.
        
        Args:
            query (str): The search query string
            filters (dict, optional): Dictionary of filters to apply to the search
            n_results (int, optional): Number of results to return
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: The search results from the OpenAlex API
        """
        params = self.translate_request(query, filters=filters, n_results=n_results)
        if kwargs:
            params.update(kwargs)
        endpoint = "authors"
        raw_response = self.make_request(endpoint, params)
        return self.translate_response(raw_response=raw_response)
    
    def get_author_id(self,author_name: str) -> str:
        author_link = self.search(author_name)[0]["id"]
        return author_link.split("https://openalex.org/")[1]

class InstititionHandler(BaseOpenAlexHandler):
    
    def search(self, query: str, filters: dict = None, n_results: Optional[int] = None, **kwargs):
        """
        Searches the OpenAlex API for institutions with the given query and filters.
        
        Args:
            query (str): The search query string
            filters (dict, optional): Dictionary of filters to apply to the search
            n_results (int, optional): Number of results to return
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: The search results from the OpenAlex API
        """
        params = self.translate_request(query, filters=filters, n_results=n_results)
        if kwargs:
            params.update(kwargs)
        endpoint = "institutions"
        raw_response = self.make_request(endpoint, params)
        return self.translate_response(raw_response=raw_response)
    
    def get_institution_id(self, institution_name: str) -> str:
        institution_link = self.search(institution_name)[0]["id"]
        return institution_link.split("https://openalex.org/")[1]

class TopicHandler(BaseOpenAlexHandler):
    
    def search(self, query: str, filters: dict = None, n_results: Optional[int] = None, **kwargs):
        """
        Searches the OpenAlex API for topics with the given query and filters.
        
        Args:
            query (str): The search query string
            filters (dict, optional): Dictionary of filters to apply to the search
            n_results (int, optional): Number of results to return
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            list: The search results from the OpenAlex API
        """
        params = self.translate_request(query, filters=filters, n_results=n_results)
        if kwargs:
            params.update(kwargs)
        endpoint = "topics"
        raw_response = self.make_request(endpoint, params)
        return self.translate_response(raw_response=raw_response)
    
    def get_topic_id(self, topic_name: str) -> str:
        topic_link = self.search(topic_name)[0]["id"]
        return topic_link.split("https://openalex.org/")[1]
    

class IDHandler(BaseOpenAlexHandler):
    '''
    lighteight handler meant to get ids from their respective names
    '''
    
    def get_author_id(self,author_name: str) -> str:
        author_link = self.search(author_name, endpoint="authors")[0]["id"]
        return author_link.split("https://openalex.org/")[1]
    
    def get_institution_id(self, institution_name: str) -> str:
        institution_link = self.search(institution_name, endpoint="institutions")[0]["id"]
        return institution_link.split("https://openalex.org/")[1]
    
    def get_topic_id(self, topic_name: str) -> str:
        results = self.search(topic_name, endpoint="topics")
        if results:
            topic_link = self.search(topic_name, endpoint="topics")[0]["id"]
            return topic_link.split("https://openalex.org/")[1]
        return


if __name__ == '__main__':
    wh = WorksHandler("sunny@scholium.ai")
    works = wh.search("BERT", filters={},n_results=10)
    assert len(works) == 10

    ah = AuthorHandler("sunny@scholium.ai")
    author = ah.get_author_id("carl sagan")
    assert author == "A5069290754"

    ih = InstititionHandler("sunny@scholium.ai")
    institution = ih.get_institution_id("university of toronto")
    assert institution == "I185261750"
    
    th = TopicHandler("sunny@scholium.ai")
    topic = th.get_topic_id("machine learning")
    assert topic == "T12072"
    
    idh = IDHandler("sunny@scholium.ai")
    author = idh.get_author_id("carl sagan")
    assert author == "A5069290754"

    institution = idh.get_institution_id("university of toronto")
    assert institution == "I185261750"
    
    topic = idh.get_topic_id("machine learning")
    assert topic == "T12072"



