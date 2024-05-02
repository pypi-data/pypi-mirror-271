"""Task(s) for the transfer and publishing of L1 data from a production run of a processing pipeline."""
import logging
from pathlib import Path
from typing import Iterable

from dkist_processing_common.models.message import CatalogFrameMessage
from dkist_processing_common.models.message import CatalogObjectMessage
from dkist_processing_common.models.message import CreateQualityReportMessage
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks.mixin.globus import GlobusMixin
from dkist_processing_common.tasks.mixin.interservice_bus import InterserviceBusMixin


__all__ = [
    "AddDatasetReceiptAccount",
    "PublishCatalogAndQualityMessages",
    "TransferL1Data",
    "L1OutputDataBase",
    "SubmitQuality",
]

from dkist_processing_common.tasks.mixin.quality import QualityMixin
from dkist_processing_common.tasks.output_data_base import OutputDataBase, TransferDataBase

logger = logging.getLogger(__name__)


class L1OutputDataBase(OutputDataBase, QualityMixin):
    """Subclass of OutputDataBase which encapsulates common level 1 output data methods."""

    @property
    def dataset_has_quality_report(self) -> bool:
        """Return True if a quality report has been submitted to the metadata-store."""
        return self.metadata_store_quality_report_exists(dataset_id=self.constants.dataset_id)

    def rollback(self):
        """Warn that the metadata-store and the interservice bus retain the effect of this tasks execution.  Rolling back this task may not be achievable without other action."""
        super().rollback()
        logger.warning(
            f"Modifications to the metadata store and the interservice bus were not rolled back."
        )


class TransferL1Data(TransferDataBase, GlobusMixin):
    """Task class for transferring Level 1 processed data to the object store."""

    def transfer_objects(self):
        """Transfer movie and L1 output frames."""
        with self.apm_task_step("Upload movie"):
            # Movie needs to be transferred separately as the movie headers need to go with it
            self.transfer_movie()

        with self.apm_task_step("Upload science frames"):
            self.transfer_output_frames()

    def transfer_output_frames(self):
        """Create a Globus transfer for all output data."""
        transfer_items = self.build_output_frame_transfer_list()

        logger.info(
            f"Preparing globus transfer {len(transfer_items)} items: "
            f"recipe_run_id={self.recipe_run_id}. "
            f"transfer_items={transfer_items[:3]}..."
        )

        self.globus_transfer_scratch_to_object_store(
            transfer_items=transfer_items,
            label=f"Transfer science frames for recipe_run_id {self.recipe_run_id}",
        )

    def transfer_movie(self):
        """Transfer the movie to the object store."""
        paths = list(self.read(tags=[Tag.output(), Tag.movie()]))
        if len(paths) == 0:
            logger.warning(
                f"No movies found to upload for dataset. recipe_run_id={self.recipe_run_id}"
            )
            return
        movie = paths[0]
        if count := len(paths) > 1:
            # note: this needs to be an error or the dataset receipt accounting will have an
            # expected count > the eventual actual
            raise RuntimeError(
                f"Multiple movies found to upload.  Uploading the first one. "
                f"{count=}, {movie=}, recipe_run_id={self.recipe_run_id}"
            )
        logger.info(f"Uploading Movie: recipe_run_id={self.recipe_run_id}, {movie=}")
        movie_object_key = self.format_object_key(movie)
        self.object_store_upload_movie(
            movie=movie,
            bucket=self.destination_bucket,
            object_key=movie_object_key,
            content_type="video/mp4",
        )


class PublishCatalogAndQualityMessages(L1OutputDataBase, InterserviceBusMixin):
    """Task class for publishing Catalog and Quality Messages."""

    def frame_messages(self, paths: Iterable[Path]) -> list[CatalogFrameMessage]:
        """
        Create the frame messages.

        Parameters
        ----------
        paths
            The input paths for which to publish frame messages

        Returns
        -------
        A list of frame messages
        """
        messages = [
            CatalogFrameMessage(
                objectName=self.format_object_key(path=p),
                conversationId=str(self.recipe_run_id),
                bucket=self.destination_bucket,
            )
            for p in paths
        ]
        return messages

    def object_messages(
        self, paths: Iterable[Path], object_type: str
    ) -> list[CatalogObjectMessage]:
        """
        Create the object messages.

        Parameters
        ----------
        paths
            The input paths for which to publish object messages
        object_type
            The object type

        Returns
        -------
        A list of object messages
        """
        messages = [
            CatalogObjectMessage(
                objectType=object_type,
                objectName=self.format_object_key(p),
                bucket=self.destination_bucket,
                conversationId=str(self.recipe_run_id),
                groupId=self.constants.dataset_id,
            )
            for p in paths
        ]
        return messages

    @property
    def quality_report_message(self) -> CreateQualityReportMessage:
        """Create the Quality Report Message."""
        file_name = Path(f"{self.constants.dataset_id}_quality_report.pdf")
        return CreateQualityReportMessage(
            bucket=self.destination_bucket,
            objectName=self.format_object_key(file_name),
            conversationId=str(self.recipe_run_id),
            datasetId=self.constants.dataset_id,
            incrementDatasetCatalogReceiptCount=True,
        )

    def run(self) -> None:
        """Run method for this trask."""
        with self.apm_task_step("Gather output data"):
            frames = self.read(tags=self.output_frame_tags)
            movies = self.read(tags=[Tag.output(), Tag.movie()])
        with self.apm_task_step("Create message objects"):
            messages = []
            messages += self.frame_messages(paths=frames)
            frame_message_count = len(messages)
            messages += self.object_messages(paths=movies, object_type="MOVIE")
            object_message_count = len(messages) - frame_message_count
            dataset_has_quality_report = self.dataset_has_quality_report
            if dataset_has_quality_report:
                messages.append(self.quality_report_message)
        with self.apm_task_step(
            f"Publish messages: {frame_message_count = }, {object_message_count = }, {dataset_has_quality_report = }"
        ):
            self.interservice_bus_publish(messages=messages)


class AddDatasetReceiptAccount(L1OutputDataBase):
    """
    Add a Dataset Receipt Account record to Processing Support for use by the Dataset Catalog Locker.

    Adds the number of files created during the calibration processing to the Processing Support table
    for use by the Dataset Catalog Locker.
    """

    def run(self) -> None:
        """Run method for this task."""
        with self.apm_processing_step("Count Expected Outputs"):
            dataset_id = self.constants.dataset_id
            expected_object_count = self.count(tags=Tag.output())
            if self.dataset_has_quality_report:
                expected_object_count += 1
        logger.info(
            f"Adding Dataset Receipt Account: "
            f"{dataset_id=}, {expected_object_count=}, recipe_run_id={self.recipe_run_id}"
        )
        with self.apm_task_step(
            f"Add Dataset Receipt Account: {dataset_id = }, {expected_object_count = }"
        ):
            self.metadata_store_add_dataset_receipt_account(
                dataset_id=dataset_id, expected_object_count=expected_object_count
            )


class SubmitQuality(L1OutputDataBase, QualityMixin):
    """Task class for submitting the quality report to the metadata store."""

    @property
    def polcal_label_list(self) -> list[str] | None:
        """Return the list of labels to look for when building polcal metrics.

        If no labels are specified then no polcal metrics will be built.
        """
        return None

    def run(self):
        """Run method for the task."""
        with self.apm_processing_step("Building quality report"):
            report = self.quality_build_report(polcal_label_list=self.polcal_label_list)
        with self.apm_task_step(f"Submitting quality report: report section count = {len(report)}"):
            self.metadata_store_add_quality_report(
                dataset_id=self.constants.dataset_id, quality_report=report
            )
