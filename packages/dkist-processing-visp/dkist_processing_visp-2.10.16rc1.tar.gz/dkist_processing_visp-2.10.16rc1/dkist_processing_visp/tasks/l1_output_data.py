"""Subclass of SubmitQuality that causes the correct polcal metrics to build."""
from dkist_processing_common.tasks import SubmitQuality

__all__ = ["VispSubmitQuality"]


class VispSubmitQuality(SubmitQuality):
    """Subclass just so that the polcal_label_list can be populated."""

    @property
    def polcal_label_list(self) -> list[str]:
        """Return labels for beams 1 and 2."""
        return ["Beam 1", "Beam 2"]
