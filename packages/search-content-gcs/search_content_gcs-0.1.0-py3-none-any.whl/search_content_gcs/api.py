from googleapiclient.discovery import build

from search_content_gcs.error import ErrorMessage, ErrorCode
from search_content_gcs.exception import SearchContentGCSApiException
from search_content_gcs.parser import parse_search_result


class SearchContentGCSApi(object):
    def __init__(self,
                *,
                api_key:str=None,
                cse_id:str=None):
        self._api_key = api_key
        self._cse_id = cse_id
        if api_key is None or cse_id is None:
            raise SearchContentGCSApiException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Must specify either client key info or api key.",
                )
            )
        # self._client = Client(api_keys=api_keys)


    def search(self,
               *
               query,
               **kwargs
               ):
        service = build("customsearch", "v1", developerKey=self._api_key)
        res = service.cse().list(q=query, cx=self._cse_id, **kwargs).execute()
        return parse_search_result(res)

