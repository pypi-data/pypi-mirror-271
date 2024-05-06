from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field


# 유튜브 비디오의 메타데이터를 위한 모델
class MetaTag(BaseModel):
    apple_itunes_app: Optional[str] = Field(None, alias='apple-itunes-app')
    og_url: Optional[HttpUrl] = Field(None, alias='og:url')
    theme_color: Optional[str] = Field(None, alias='theme-color')
    twitter_url: Optional[HttpUrl] = Field(None, alias='twitter:url')
    viewport: Optional[str] = Field(None)

class PageMap(BaseModel):
    cse_image: List[dict]
    cse_thumbnail: List[dict]
    metatags: List[MetaTag]

class Item(BaseModel):
    cacheId: Optional[str] = Field(None)
    displayLink: str
    formattedUrl: HttpUrl
    htmlFormattedUrl: HttpUrl
    htmlSnippet: str
    htmlTitle: str
    kind: str
    link: HttpUrl
    pagemap: PageMap
    snippet: str
    title: str

class QueryRequest(BaseModel):
    count: int
    cx: str
    inputEncoding: str
    outputEncoding: str
    safe: str
    searchTerms: str
    startIndex: int
    title: str
    totalResults: str

class Queries(BaseModel):
    request: List[QueryRequest]

class SearchInformation(BaseModel):
    formattedSearchTime: str
    formattedTotalResults: str
    searchTime: float
    totalResults: Optional[str] = Field(None)

class Response(BaseModel):
    context: dict
    items: Optional[List[Item]] = Field([])
    kind: str
    queries: Queries
    searchInformation: SearchInformation
    url: dict

