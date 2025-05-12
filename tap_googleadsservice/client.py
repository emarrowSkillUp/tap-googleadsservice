"""Custom client handling, including googleadsserviceStream base class."""

from __future__ import annotations

import typing as t

from singer_sdk.streams import Stream

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


class GoogleAdsServiceStream(Stream):
    """Stream class for googleads-service streams."""

    def get_records(
        self,
        context: Context | None,
    ) -> t.Iterable[dict]:
        """Return a generator of record-type dictionary objects.

        The optional `context` argument is used to identify a specific slice of the
        stream if partitioning is required for the stream. Most implementations do not
        require partitioning and should ignore the `context` argument.

        Args:
            context: Stream partition or context dictionary.

        Raises:
            NotImplementedError: If the implementation is TODO
        """
        errmsg = "The method is not yet implemented (TODO)"
        raise NotImplementedError(errmsg)
