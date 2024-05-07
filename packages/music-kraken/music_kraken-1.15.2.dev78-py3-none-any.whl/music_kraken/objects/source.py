from __future__ import annotations

from collections import defaultdict
from enum import Enum
from typing import List, Dict, Set, Tuple, Optional, Iterable, Generator
from urllib.parse import urlparse, ParseResult
from dataclasses import dataclass, field
from functools import cached_property

from ..utils import generate_id
from ..utils.enums.source import SourcePages, SourceTypes
from ..utils.config import youtube_settings
from ..utils.string_processing import hash_url, shorten_display_url

from .metadata import Mapping, Metadata
from .parents import OuterProxy
from .collection import Collection



@dataclass
class Source:
    page_enum: SourcePages
    url: str
    referrer_page: SourcePages = None
    audio_url: Optional[str] = None

    additional_data: dict = field(default_factory=dict)

    def __post_init__(self):
        self.referrer_page = self.referrer_page or self.page_enum
    
    @property
    def parsed_url(self) -> ParseResult:
        return urlparse(self.url)

    @classmethod
    def match_url(cls, url: str, referrer_page: SourcePages) -> Optional[Source]:
        """
        this shouldn't be used, unless you are not certain what the source is for
        the reason is that it is more inefficient
        """
        parsed_url = urlparse(url)
        url = parsed_url.geturl()
        
        if "musify" in parsed_url.netloc:
            return cls(SourcePages.MUSIFY, url, referrer_page=referrer_page)

        if parsed_url.netloc in [_url.netloc for _url in youtube_settings['youtube_url']]:
            return cls(SourcePages.YOUTUBE, url, referrer_page=referrer_page)

        if url.startswith("https://www.deezer"):
            return cls(SourcePages.DEEZER, url, referrer_page=referrer_page)
        
        if url.startswith("https://open.spotify.com"):
            return cls(SourcePages.SPOTIFY, url, referrer_page=referrer_page)

        if "bandcamp" in url:
            return cls(SourcePages.BANDCAMP, url, referrer_page=referrer_page)

        if "wikipedia" in parsed_url.netloc:
            return cls(SourcePages.WIKIPEDIA, url, referrer_page=referrer_page)

        if url.startswith("https://www.metal-archives.com/"):
            return cls(SourcePages.ENCYCLOPAEDIA_METALLUM, url, referrer_page=referrer_page)

        # the less important once
        if url.startswith("https://www.facebook"):
            return cls(SourcePages.FACEBOOK, url, referrer_page=referrer_page)

        if url.startswith("https://www.instagram"):
            return cls(SourcePages.INSTAGRAM, url, referrer_page=referrer_page)

        if url.startswith("https://twitter"):
            return cls(SourcePages.TWITTER, url, referrer_page=referrer_page)

        if url.startswith("https://myspace.com"):
            return cls(SourcePages.MYSPACE, url, referrer_page=referrer_page)

    @property
    def hash_url(self) -> str:
        return hash_url(self.url)

    @property
    def indexing_values(self) -> list:
        r = [hash_url(self.url)]
        if self.audio_url:
            r.append(hash_url(self.audio_url))
        return r

    def __repr__(self) -> str:
        return f"Src({self.page_enum.value}: {shorten_display_url(self.url)})"

    def __merge__(self, other: Source, **kwargs):
        if self.audio_url is None:
            self.audio_url = other.audio_url
        self.additional_data.update(other.additional_data)

    page_str = property(fget=lambda self: self.page_enum.value)


class SourceCollection:
    __change_version__ = generate_id()

    _indexed_sources: Dict[str, Source]
    _page_to_source_list: Dict[SourcePages, List[Source]]

    def __init__(self, data: Optional[Iterable[Source]] = None, **kwargs):
        self._page_to_source_list = defaultdict(list)
        self._indexed_sources = {}

        self.extend(data or [])

    def has_source_page(self, *source_pages: SourcePages) -> bool:
        return any(source_page in self._page_to_source_list for source_page in source_pages)

    def get_sources(self, *source_pages: List[Source]) -> Generator[Source]:
        if not len(source_pages):
            source_pages = self.source_pages

        for page in source_pages:
            yield from self._page_to_source_list[page]

    def append(self, source: Source):
        if source is None:
            return

        existing_source = None
        for key in source.indexing_values:
            if key in self._indexed_sources:
                existing_source = self._indexed_sources[key]
                break

        if existing_source is not None:
            existing_source.__merge__(source)
            source = existing_source
        else:
            self._page_to_source_list[source.page_enum].append(source)

        changed = False
        for key in source.indexing_values:
            if key not in self._indexed_sources:
                changed = True
            self._indexed_sources[key] = source

        if changed:
            self.__change_version__ = generate_id()

    def extend(self, sources: Iterable[Source]):
        for source in sources:
            self.append(source)

    def __iter__(self):
        yield from self.get_sources()

    def __merge__(self, other: SourceCollection, **kwargs):
        self.extend(other)
        
    @property
    def source_pages(self) -> Iterable[SourcePages]:
        return sorted(self._page_to_source_list.keys(), key=lambda page: page.value)

    @property
    def hash_url_list(self) -> List[str]:
        return [hash_url(source.url) for source in self.get_sources()]

    @property
    def url_list(self) -> List[str]:
        return [source.url for source in self.get_sources()]

    @property
    def homepage_list(self) -> List[str]:
        return [source.homepage for source in self.source_pages]

    def indexing_values(self) -> Generator[Tuple[str, str], None, None]:
        for index in self._indexed_sources:
            yield "url", index