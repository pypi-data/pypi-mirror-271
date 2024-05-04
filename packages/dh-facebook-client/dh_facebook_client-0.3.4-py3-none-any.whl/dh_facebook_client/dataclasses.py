from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from requests import Response

from .helpers import deserialize_json_header
from .typings import GraphAPIQueryResult, JSONTypeSimple


@dataclass(frozen=True)
class AppUsageDetails:
    """
    Encapsulates stats from X-App-Usage header:
    https://developers.facebook.com/docs/graph-api/overview/rate-limiting#headers
    """

    call_count: int
    total_time: int
    total_cputime: int

    @classmethod
    def from_header(cls, res: Response) -> AppUsageDetails:
        app_usage_dict = deserialize_json_header(res=res, header_name='X-App-Usage')
        return cls(
            call_count=app_usage_dict.get('call_count', 0),
            total_time=app_usage_dict.get('total_time', 0),
            total_cputime=app_usage_dict.get('total_cputime', 0),
        )


@dataclass(frozen=True)
class MarketingAPIThrottleInsights:
    """
    Encapsulates stats from X-Fb-Ads-Insights-Throttle header:
    https://developers.facebook.com/docs/marketing-api/insights/best-practices/#insightscallload
    """

    app_id_util_pct: float
    acc_id_util_pct: float
    ads_api_access_tier: str

    @classmethod
    def from_header(cls, res: Response) -> MarketingAPIThrottleInsights:
        throttle_insights_dict = deserialize_json_header(
            res=res, header_name='X-Fb-Ads-Insights-Throttle'
        )
        return cls(
            app_id_util_pct=throttle_insights_dict.get('app_id_util_pct', 0.0),
            acc_id_util_pct=throttle_insights_dict.get('acc_id_util_pct', 0.0),
            ads_api_access_tier=throttle_insights_dict.get('ads_api_access_tier', ''),
        )


@dataclass
class GraphAPIResponse:
    """
    Encapsulates a Graph API response payload with parsed app usage headers
    """

    app_usage_details: AppUsageDetails
    marketing_api_throttle_insights: MarketingAPIThrottleInsights
    data: GraphAPIQueryResult
    paging: Optional[JSONTypeSimple] = None

    @property
    def is_empty(self) -> bool:
        return not self.data

    @property
    def is_list(self) -> bool:
        return isinstance(self.data, list)

    @property
    def is_dict(self) -> bool:
        return isinstance(self.data, dict)

    @property
    def before_cursor(self) -> Optional[str]:
        return self.cursors.get('before')

    @property
    def after_cursor(self) -> Optional[str]:
        return self.cursors.get('after')

    @property
    def next_page_url(self) -> Optional[str]:
        return self.paging.get('next') if self.paging else None

    @property
    def cursors(self) -> JSONTypeSimple:
        return self.paging.get('cursors', {}) if self.paging else {}
