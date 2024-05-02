"""Quality task definition."""
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks import QualityL0Metrics
from dkist_processing_common.tasks import SubmitQuality

__all__ = ["TestQualityL0Metrics", "TestSubmitQuality"]


class TestQualityL0Metrics(QualityL0Metrics):
    def run(self) -> None:
        paths = self.read(tags=[Tag.input()])
        self.calculate_l0_metrics(paths=paths)


class TestSubmitQuality(SubmitQuality):
    @property
    def polcal_label_list(self) -> list[str] | None:
        return ["Beam1"]
