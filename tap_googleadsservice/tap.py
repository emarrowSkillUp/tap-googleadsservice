"""googleadsservice tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_googleadsservice import streams


class Tapgoogleadsservice(Tap):
    """googleadsservice tap class."""

    name = "tap-googleadsservice"

    # TODO: Update this section with the actual config values you expect:
    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "yaml_path",
            th.StringType(nullable=False),
            required=True,
            title="Yaml Path",
            description="Path to google-ads.yaml file",
        ),
        th.Property(
            "manager_account_id",
            th.StringType(nullable=False),
            required=True,
            title="Manager Account ID",
            description="ID of Google Ads Manager Account",
        ),
        th.Property(
            "customer_id",
            th.StringType(nullable=False),
            required=True,
            title="Customer ID",
            description="ID of Google Ads Manager Account",
        ),
        th.Property(
            "start_date",
            th.DateType(nullable=True),
            description="The earliest record date to sync",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.googleadsserviceStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.CampaignsStream(self)
        ]


if __name__ == "__main__":
    Tapgoogleadsservice.cli()
