from pathlib import Path
from datetime import datetime
import shutil

from src.audit_logger import log_retention


def archive_file(file_path):
    """
    Moves a processed file into the retention/archive folder.
    """

    source_path = Path(file_path)

    # --------------------------------
    # Check that source file exists
    # --------------------------------

    if not source_path.exists():

        raise FileNotFoundError(
            f"File not found: {source_path}"
        )

    # --------------------------------
    # Create archive folder
    # --------------------------------

    archive_directory = Path(
        "data/retention/archive"
    )

    archive_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    try:

        # --------------------------------
        # Create timestamp
        # --------------------------------

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        # --------------------------------
        # Create archive filename
        # --------------------------------

        archive_filename = (
            f"{source_path.stem}_"
            f"{timestamp}"
            f"{source_path.suffix}"
        )

        destination_path = (
            archive_directory /
            archive_filename
        )

        # --------------------------------
        # Move file
        # --------------------------------

        shutil.move(
            str(source_path),
            str(destination_path)
        )

        # --------------------------------
        # Write successful log
        # --------------------------------

        log_retention(
            file_name=source_path.name,
            status="SUCCESS",
            row_count=None,
            message=(
                f"Archived to "
                f"{destination_path}"
            )
        )

        print()
        print(
            "Archive successful:"
        )

        print(
            destination_path
        )

        return destination_path

    except Exception as error:

        # --------------------------------
        # Write failed log
        # --------------------------------

        log_retention(
            file_name=source_path.name,
            status="FAILED",
            row_count=None,
            message=str(error)
        )

        print(
            f"Archive failed: {error}"
        )

        raise