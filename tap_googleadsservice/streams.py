"""Stream type classes for tap-googleadsservice."""

from __future__ import annotations

import typing as t
from importlib import resources
from datetime import datetime, timedelta

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_googleadsservice.client import GoogleAdsServiceStream

from google.ads.googleads.client import GoogleAdsClient

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context

class CampaignsStream(GoogleAdsServiceStream):
    """Define custom stream."""

    replication_key = "date"
    is_sorted = True
    name = "campaigns"
    primary_keys: t.ClassVar[list[str]] = ["campaign_id", "date"]
    schema = th.PropertiesList(
        th.Property(
            "campaign_id",
            th.IntegerType,
        ),
        th.Property(
            "campaign_name",
            th.StringType,
        ),
        th.Property(
            "date",
            th.StringType,
        ),
        th.Property(
            "impressions",
            th.IntegerType
        ),
        th.Property(
            "clicks",
            th.IntegerType
        ),
        th.Property(
            "cost_micros",
            th.IntegerType
        )
    ).to_dict()

    def get_gaql(self, context: Context | None):
        starting_date = self.get_starting_replication_key_value(context)
        end_date = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
        if starting_date:
            return f"""
                SELECT
                    campaign.id,
                    campaign.name,
                    segments.date,
                    metrics.impressions,
                    metrics.clicks,
                    metrics.cost_micros
                FROM campaign
                WHERE segments.date DURING LAST_30_DAYS
                ORDER BY segments.date
            """
        else:
            return f"""
                SELECT
                    campaign.id,
                    campaign.name,
                    segments.date,
                    metrics.impressions,
                    metrics.clicks,
                    metrics.cost_micros
                FROM campaign
                WHERE segments.date BETWEEN '{self.config['start_date']}' AND '{end_date}'
                ORDER BY segments.date
            """

    def get_records(self, context: Context | None) -> t.Iterable[dict]:
        """Return a generator of record-type dictionary objects.

        The optional `context` argument is used to identify a specific slice of the
        stream if partitioning is required for the stream. Most implementations do not
        require partitioning and should ignore the `context` argument.

        Args:
            context: Stream partition or context dictionary.
        """
        ga_client = GoogleAdsClient.load_from_storage(self.config['yaml_path'])
        ga_service = ga_client.get_service("GoogleAdsService")

        response = ga_service.search(customer_id=self.config['customer_id'], query=self.get_gaql(context))
        for row in response:
            yield {
                'campaign_id': row.campaign.id,
                'campaign_name': row.campaign.name,
                'date': row.segments.date,
                'impressions': row.metrics.impressions,
                'clicks': row.metrics.clicks,
                'cost_micros': row.metrics.cost_micros
            }

