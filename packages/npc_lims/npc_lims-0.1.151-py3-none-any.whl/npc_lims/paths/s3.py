from __future__ import annotations

import contextlib
import dataclasses
import functools
import operator
from collections.abc import Iterator

import npc_session
import upath

import npc_lims.metadata.codeocean as codeocean
import npc_lims.status.tracked_sessions as tracked_sessions

DR_DATA_REPO = upath.UPath(
    "s3://aind-scratch-data/ben.hardcastle/DynamicRoutingTask/Data"
)
NWB_REPO = upath.UPath("s3://aind-scratch-data/ben.hardcastle/nwb/nwb")

S3_SCRATCH_ROOT = upath.UPath("s3://aind-scratch-data/ben.hardcastle")

TISSUECYTE_REPO = upath.UPath(
    "s3://aind-scratch-data/arjun.sridhar/tissuecyte_cloud_processed"
)

CODE_OCEAN_DATA_BUCKET = upath.UPath("s3://codeocean-s3datasetsbucket-1u41qdg42ur9")

VIDEO_SUFFIXES = (".mp4", ".avi", ".wmv", ".mov")


def get_data_asset_s3_path(asset_id: str | codeocean.DataAssetAPI) -> upath.UPath:
    """Path on s3 that contains actual data for CodeOcean data asset.

    - asset `id` is a UUID
    - accept anything with an "id" attribute or key, or a string
    Assumes that the data asset has data on s3, which may not be true, and we can't tell from asset info.
    """
    bucket = CODE_OCEAN_DATA_BUCKET
    with contextlib.suppress(AttributeError, KeyError, TypeError):
        bucket = upath.UPath(upath.UPath(f's3://{asset_id["source_bucket"]}'))  # type: ignore[index]
    with contextlib.suppress(AttributeError, KeyError):
        return bucket / asset_id.get("id")  # type: ignore[union-attr, operator]
    with contextlib.suppress(AttributeError):
        return bucket / asset_id.id  # type: ignore[union-attr]
    return bucket / str(asset_id)


@functools.cache
def get_raw_data_paths_from_s3(
    session: str | npc_session.SessionRecord,
) -> tuple[upath.UPath, ...]:
    """All top-level files and folders from the `ephys` & `behavior`
    subdirectories in a session's raw data folder on s3.

    Examples:
        >>> files = get_raw_data_paths_from_s3 ('668759_20230711')
        >>> assert len(files) > 0
    """
    raw_data_root = codeocean.get_raw_data_root(session)
    directories: Iterator[upath.UPath] = (
        directory for directory in raw_data_root.iterdir() if directory.is_dir()
    )
    first_level_files_directories: Iterator = (
        tuple(directory.iterdir()) for directory in directories
    )

    paths = functools.reduce(operator.add, first_level_files_directories)

    if not paths:
        raise FileNotFoundError(
            f"Raw data paths empty for {session} on s3. Looks like an upload was started, but no files have been transferred."
        )
    return paths


@functools.cache
def get_sorted_data_paths_from_s3(
    session: str | npc_session.SessionRecord | None = None,
    sorted_data_asset_id: str | None = None,
) -> tuple[upath.UPath, ...]:
    """
    Gets the top level files/folders for the sorted data

    Examples:
        >>> sorted_data_s3_paths = get_sorted_data_paths_from_s3('668759_20230711')
        >>> assert len(sorted_data_s3_paths) > 0
    """
    if sorted_data_asset_id is not None:
        sorted_data_asset = codeocean.get_data_asset(sorted_data_asset_id)
    elif session is not None:
        sorted_data_asset = codeocean.get_session_sorted_data_asset(session)
    else:
        raise ValueError("Must provide either session or sorted_data_asset_id")
    return tuple(get_data_asset_s3_path(sorted_data_asset).iterdir())


@functools.cache
def get_dlc_eye_s3_paths(
    session: str | npc_session.SessionRecord,
) -> tuple[upath.UPath, ...]:
    """
    >>> paths = get_dlc_eye_s3_paths('676909_2023-12-13')
    >>> len(paths)
    8
    """
    session = npc_session.SessionRecord(session)
    dlc_eye_data_asset = codeocean.get_session_capsule_pipeline_data_asset(
        session, "dlc_eye"
    )

    return tuple(get_data_asset_s3_path(dlc_eye_data_asset).iterdir())


@functools.cache
def get_dlc_side_s3_paths(
    session: str | npc_session.SessionRecord,
) -> tuple[upath.UPath, ...]:
    """
    >>> paths = get_dlc_side_s3_paths('676909_2023-12-13')
    >>> len(paths)
    5
    """
    session = npc_session.SessionRecord(session)
    dlc_side_data_asset = codeocean.get_session_capsule_pipeline_data_asset(
        session, "dlc_side"
    )

    return tuple(get_data_asset_s3_path(dlc_side_data_asset).iterdir())


@functools.cache
def get_dlc_face_s3_paths(
    session: str | npc_session.SessionRecord,
) -> tuple[upath.UPath, ...]:
    """
    >>> paths = get_dlc_face_s3_paths('676909_2023-12-13')
    >>> len(paths)
    5
    """
    session = npc_session.SessionRecord(session)
    dlc_face_data_asset = codeocean.get_session_capsule_pipeline_data_asset(
        session, "dlc_face"
    )

    return tuple(get_data_asset_s3_path(dlc_face_data_asset).iterdir())


@functools.cache
def get_facemap_s3_paths(
    session: str | npc_session.SessionRecord,
) -> tuple[upath.UPath, ...]:
    """
    >>> paths = get_facemap_s3_paths('646318_2023-01-17')
    >>> len(paths)
    6
    """
    session = npc_session.SessionRecord(session)
    facemap_data_asset = codeocean.get_session_capsule_pipeline_data_asset(
        session, "facemap"
    )

    return tuple(get_data_asset_s3_path(facemap_data_asset).iterdir())


@functools.cache
def get_settings_xml_path_from_s3(
    session: str | npc_session.SessionRecord,
) -> upath.UPath:
    """
    Examples:
        >>> settings_xml_path = get_settings_xml_path_from_s3('670180-2023-07-26')
        >>> assert settings_xml_path.exists()
    """
    raw_data_paths_s3 = get_raw_data_paths_from_s3(session)

    directories = (
        raw_path
        for raw_path in raw_data_paths_s3
        if raw_path.is_dir() and ".zarr" not in raw_path.suffix
    )
    return tuple(raw_path / "settings.xml" for raw_path in directories)[0]


@functools.cache
def get_h5_sync_from_s3(session: str | npc_session.SessionRecord) -> upath.UPath:
    """
    Examples:
        >>> get_h5_sync_from_s3('662892_20230821')
        S3Path('s3://aind-ephys-data/ecephys_662892_2023-08-21_12-43-45/behavior/20230821T124345.h5')
    """
    raw_data_paths_s3 = get_raw_data_paths_from_s3(session)
    sync_path = tuple(path for path in raw_data_paths_s3 if ".h5" in path.suffix)

    if not sync_path:
        raise FileNotFoundError(f"No sync file found in {raw_data_paths_s3!r}")

    return sync_path[0]


@functools.cache
def get_recording_dirs_experiment_path_from_s3(
    session: str | npc_session.SessionRecord,
) -> tuple[upath.UPath, ...]:
    """
    Examples:
        >>> recording_dirs = get_recording_dirs_experiment_path_from_s3('662892_20230821')
        >>> assert len(recording_dirs) > 0
    """
    raw_data_paths = get_raw_data_paths_from_s3(session)
    recording_dirs = (
        path
        for path in raw_data_paths
        if "Record Node" in str(path) and "zarr" not in str(path)
    )
    recording_dirs_experiment = tuple(
        next(path.glob("*/recording*")) for path in recording_dirs
    )

    return recording_dirs_experiment


@functools.cache
def get_behavior_video_path_from_s3(
    session: str | npc_session.SessionRecord,
) -> upath.UPath:
    """
    >>> get_behavior_video_path_from_s3('686740_2023-10-26')
    S3Path('s3://aind-ephys-data/ecephys_686740_2023-10-26_12-29-08/behavior_videos/Behavior_20231026T122922.mp4')
    """
    raw_data_paths = get_raw_data_paths_from_s3(session)
    behavior_video_path = tuple(
        path
        for path in raw_data_paths
        if "Behavior" in path.stem and path.suffix in VIDEO_SUFFIXES
    )

    if not behavior_video_path:
        raise FileNotFoundError(f"{session} has no behavior video on s3")

    return behavior_video_path[0]


@functools.cache
def get_eye_video_path_from_s3(session: str | npc_session.SessionRecord) -> upath.UPath:
    """
    >>> get_eye_video_path_from_s3('686740_2023-10-26')
    S3Path('s3://aind-ephys-data/ecephys_686740_2023-10-26_12-29-08/behavior_videos/Eye_20231026T122922.mp4')
    """
    raw_data_paths = get_raw_data_paths_from_s3(session)
    eye_video_path = tuple(
        path
        for path in raw_data_paths
        if "Eye" in path.stem and path.suffix in VIDEO_SUFFIXES
    )

    if not eye_video_path:
        raise FileNotFoundError(f"{session} has no eye video on s3")

    return eye_video_path[0]


@functools.cache
def get_face_video_path_from_s3(
    session: str | npc_session.SessionRecord,
) -> upath.UPath:
    """
    >>> get_face_video_path_from_s3('686740_2023-10-26')
    S3Path('s3://aind-ephys-data/ecephys_686740_2023-10-26_12-29-08/behavior_videos/Face_20231026T122923.mp4')
    """
    raw_data_paths = get_raw_data_paths_from_s3(session)
    face_video_path = tuple(
        path
        for path in raw_data_paths
        if "Face" in path.stem and path.suffix in VIDEO_SUFFIXES
    )

    if not face_video_path:
        raise FileNotFoundError(f"{session} has no face video on s3")

    return face_video_path[0]


@functools.cache
def get_tissuecyte_annotation_files_from_s3(
    session: str | npc_session.SessionRecord,
) -> tuple[upath.UPath, ...]:
    """For each probe inserted, get a csv file containing CCF coordinates for each
    electrode (channel) on the probe.

    Examples:
        >>> electrode_files = get_tissuecyte_annotation_files_from_s3('626791_2022-08-16')
        >>> assert len(electrode_files) > 0
        >>> electrode_files[0].name
        'Probe_A2_channels_626791_warped_processed_new_sorting.csv'
    """
    session = npc_session.SessionRecord(session)
    day = tracked_sessions.get_session_info(session).experiment_day
    subject_electrode_network_path = TISSUECYTE_REPO / str(session.subject.id)

    if not subject_electrode_network_path.exists():
        raise FileNotFoundError(
            f"CCF annotations for {session} have not been uploaded to s3"
        )

    electrode_files = tuple(
        subject_electrode_network_path.glob(
            f"Probe_*{day}_channels_{str(session.subject.id)}_warped_processed_new_sorting.csv"
        )
    )
    if not electrode_files:
        raise FileNotFoundError(
            f"{subject_electrode_network_path} exists, but no CCF annotation files found matching {day} and {session.subject.id} - check session day"
        )

    return electrode_files


@dataclasses.dataclass
class StimFile:
    path: upath.UPath
    session: npc_session.SessionRecord
    name = property(lambda self: self.path.stem.split("_")[0])
    date = property(lambda self: self.session.date)
    time = property(lambda self: npc_session.extract_isoformat_time(self.path.stem))
    size = functools.cached_property(lambda self: self.path.stat()["size"])


@functools.cache
def get_hdf5_stim_files_from_s3(
    session: str | npc_session.SessionRecord,
) -> tuple[StimFile, ...]:
    """All the stim files for a session, from the synced
    `DynamicRoutingTask/Data` folder on s3.

    - filters out files that are obviously wrong

    Examples:
        >>> files = get_hdf5_stim_files_from_s3('668759_20230711')
        >>> assert len(files) > 0
        >>> files[0].name, files[0].time
        ('DynamicRouting1', '13:25:00')
    """
    session = npc_session.SessionRecord(session)
    root = DR_DATA_REPO / str(session.subject)
    if not root.exists():
        if not DR_DATA_REPO.exists():
            raise FileNotFoundError(f"{DR_DATA_REPO = } does not exist")
        raise FileNotFoundError(
            f"Subject {session.subject} hdf5s not on s3: may have been run by NSB, in which case they are on lims2"
        )
    file_glob = f"*_{session.subject}_{session.date.replace('-', '')}_??????.hdf5"
    files = [StimFile(path, session) for path in root.glob(file_glob)]

    test_glob = file_glob.replace(str(session.subject), "test")
    files += [
        StimFile(path, session)
        for path in root.glob(test_glob)
        if str(session.subject) in path.as_posix()
    ]

    # no empty files:
    files = [f for f in files if f.size > 0]

    # single behavior task:
    behavior_tasks = tuple(f for f in files if "DynamicRouting" in f.name)
    if len(behavior_tasks) > 1:
        largest = max(behavior_tasks, key=lambda f: f.size)
        for f in behavior_tasks:
            if f.path != largest.path:
                files.remove(f)

    return tuple(files)


if __name__ == "__main__":
    import doctest

    doctest.testmod(
        optionflags=(doctest.IGNORE_EXCEPTION_DETAIL | doctest.NORMALIZE_WHITESPACE)
    )
