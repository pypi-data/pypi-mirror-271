import datetime
import requests
import time
from typing import Optional, List, Dict, Union

from search_content_gcs.error import ErrorCode, ErrorMessage
from search_content_gcs.exception import SearchContentGCSApiException
from search_content_gcs.models import Response

APIKeys = List[Dict[str, str]]


class Client(object):
    DEFAULT_TIMEOUT = 10

    def __init__(self,
                 api_keys: APIKeys,
                 timeout: Optional[int] = None):

        self._api_keys = api_keys
        self._timeout = timeout
        if not self._api_keys or len(self._api_keys) == 0:
            raise SearchContentGCSApiException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="Must specify either client key info or api key.",
                )
            )

        if self._timeout is None:
            self._timeout = self.DEFAULT_TIMEOUT

    def _check_if_all_key_is_expired(self):
        is_all_expired = True
        for key, value in self.api_key_usage:
            is_expired = value['expired']
            if is_expired is False:
                all_expired = False
                break
        return is_all_expired

    def _get_next_key(self):
        """다음 사용할 API 키를 반환합니다. 모든 키가 만료되었다면 대기합니다."""
        original_index = self.current_key_index
        while True:
            current_key = self.api_keys[self.current_key_index]
            if not self.api_key_usage[current_key]["expired"]:
                return current_key
            self.current_key_index = (self.current_key_index + 1) % len(self.current_key_index)
            if self.current_key_index == original_index:  # 모든 키가 만료된 경우
                print("All API keys are expired. Waiting...")
                time.sleep(self.cool_down_period)
                self._update_key_usage()  # 만료 상태 업데이트 시도

    @staticmethod
    def _parse_response(response: Response) -> dict:
        """
        Parse response data and check whether errors exists.

        Args:
            response (Response)
                The response which the request return.
        Return:
             response's data
        """
        data = response.json()
        if "error" in data:
            raise SearchContentGCSApiException(response)
        return data

    @staticmethod
    def _parse_data(data: Optional[dict]) -> Union[dict, list]:
        """
        Parse resp data.

        Args:
            data (dict)
                The response data by response.json()
        Return:
             response's items
        """
        items = data["items"]
        return items

    def _request(
            self, resource, method=None, args=None, post_args=None, enforce_auth=True
    ):
        # ) -> Response:
        """
        Main request sender.

        Args:
            resource(str)
                Resource field is which type data you want to retrieve.
                Such as channels，videos and so on.
            method(str, optional)
                The method this request to send request.
                Default is 'GET'
            args(dict, optional)
                The url params for this request.
            post_args(dict, optional)
                The Post params for this request.
            enforce_auth(bool, optional)
                Whether use google credentials
        Returns:
            response
        """
        if method is None:
            method = "GET"

        if args is None:
            args = dict()

        if post_args is not None:
            method = "POST"

        key = None
        access_token = None

        self._update_key_usage()  # 필요한 경우 쿼터 초기화
        api_key = self.api_keys[self.current_key_index]

        if api_key is not None:
            key = "key"
            access_token = api_key
        if self._access_token is not None:
            key = "access_token"
            access_token = self._access_token
        if access_token is None and enforce_auth:
            raise SearchContentGCSApiException(
                ErrorMessage(
                    status_code=ErrorCode.MISSING_PARAMS,
                    message="You must provide your credentials.",
                )
            )

        try:
            response = self.session.request(
                method=method,
                url=self.BASE_URL + resource,
                timeout=self._timeout,
                params=args,
                data=post_args,
                proxies=self.proxies,
            )
        except requests.HTTPError as e:
            if e.response.status_code == 403:  # 쿼터 초과 에러 처리
                # 현재 API 키의 쿼터가 초과되었다고 표시하고 다음 키로 전환하는 로직 추가
                self.api_key_usage[api_key] = {
                    'expired': True,
                    'reset_time': datetime.datetime.now()
                }
                is_all_key_expired = self._check_if_all_key_is_expired()
                if is_all_key_expired is True:
                    raise Exception("All key is expired ")
                else:
                    service = build("customsearch", "v1", developerKey=api_key)
                    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
                    return self._request(resource, method, args, post_args, enforce_auth)
            else:
                raise SearchContentGCSApiException(
                    ErrorMessage(status_code=ErrorCode.HTTP_ERROR, message=e.args[0])
                )
        else:
            return response
