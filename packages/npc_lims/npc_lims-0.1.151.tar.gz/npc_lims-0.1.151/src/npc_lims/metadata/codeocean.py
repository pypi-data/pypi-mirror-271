from __future__ import annotations

import functools
import logging
import os
import re
import uuid
from collections.abc import Mapping, Sequence
from typing import Any, Literal, NamedTuple, TypedDict

import npc_session
import requests
import upath
from aind_codeocean_api import codeocean as aind_codeocean_api
from aind_codeocean_api.models import data_assets_requests as aind_codeocean_requests
from aind_codeocean_api.models.computations_requests import (
    ComputationDataAsset,
    RunCapsuleRequest,
)
from typing_extensions import TypeAlias

import npc_lims.exceptions as exceptions
import npc_lims.paths.s3 as s3

logger = logging.getLogger(__name__)

DataAssetAPI: TypeAlias = dict[
    Literal[
        "created",
        "custom_metadata",
        "description",
        "files",
        "id",
        "last_used",
        "name",
        "size",
        "source_bucket",
        "state",
        "tags",
        "type",
    ],
    Any,
]
"""Result from CodeOcean API when querying data assets."""

RunCapsuleResponseAPI: TypeAlias = dict[
    Literal["created", "has_results", "id", "name", "run_time", "state"], Any
]


class CapsulePipelineInfo(NamedTuple):
    id: str
    process_name: str
    is_pipeline: bool


class CapsuleComputationAPI(TypedDict):
    """Result from CodeOceanAPI when querying for computations for a capsule"""

    """As returned from response.json()"""
    created: int
    has_results: bool
    id: str
    name: str
    run_time: int
    state: str
    end_status: str | None
    """Does not exist initially"""


ResultItemAPI: TypeAlias = dict[Literal["name", "path", "size", "type"], Any]
"""Result from CodeOceanAPI when querying for results from a computation"""

MODEL_CAPSULE_PIPELINE_MAPPING: dict[str, str] = {
    "dlc_eye": "4cf0be83-2245-4bb1-a55c-a78201b14bfe",
    "dlc_side": "facff99f-d3aa-4ecd-8ef8-a343c38197aa",
    "dlc_face": "a561aa4c-2066-4ff2-a916-0db86b918cdf",
    "facemap": "670de0b3-f73d-4d22-afe6-6449c45fada4",
    "sorting_pipeline": "1f8f159a-7670-47a9-baf1-078905fc9c2e",
}

EXAMPLE_JOB_STATUS = {
    "created": 1710962969,
    "has_results": True,
    "id": "1c900aa5-dde4-475d-bf50-cc96aff9db39",
    "name": "Run With Parameters 962969",
    "run_time": 84184,
    "state": "completed",
    "end_status": "succeeded",
}


class SessionIndexError(IndexError):
    pass


class ModelCapsuleMappingError(KeyError):
    pass


@functools.cache
def get_codeocean_client() -> aind_codeocean_api.CodeOceanClient:
    token = os.getenv(
        key="CODE_OCEAN_API_TOKEN",
        default=next(
            (v for v in os.environ.values() if v.lower().startswith("cop_")), None
        ),
    )
    if token is None:
        raise exceptions.MissingCredentials(
            "`CODE_OCEAN_API_TOKEN` not found in environment variables"
        )
    return aind_codeocean_api.CodeOceanClient(
        domain=os.getenv(
            key="CODE_OCEAN_DOMAIN",
            default="https://codeocean.allenneuraldynamics.org",
        ),
        token=token,
    )


def get_subject_data_assets(subject: str | int) -> tuple[DataAssetAPI, ...]:
    """
    All assets associated with a subject ID.

    Examples:
        >>> assets = get_subject_data_assets(668759)
        >>> assert len(assets) > 0
    """
    response = get_codeocean_client().search_all_data_assets(
        query=f"subject id: {npc_session.SubjectRecord(subject)}"
    )
    response.raise_for_status()
    return response.json()["results"]


def get_session_data_assets(
    session: str | npc_session.SessionRecord,
) -> tuple[DataAssetAPI, ...]:
    session = npc_session.SessionRecord(session)
    assets = get_subject_data_assets(session.subject)
    try:
        pattern = get_codoecean_session_id(session)
    except ValueError:  # no raw data uploaded
        pattern = f"ecephys_{session.subject}_{session.date}_{npc_session.PARSE_TIME}"
    return tuple(
        asset
        for asset in assets
        if re.match(
            f"{pattern}(_[a-z]*_[a-z]*)*",
            asset["name"],
        )
    )


def get_session_result_data_assets(
    session: str | npc_session.SessionRecord,
) -> tuple[DataAssetAPI, ...]:
    """
    Examples:
        >>> result_data_assets = get_session_result_data_assets('668759_20230711')
        >>> assert len(result_data_assets) > 0
    """
    session_data_assets = get_session_data_assets(session)
    result_data_assets = tuple(
        data_asset
        for data_asset in session_data_assets
        if data_asset["type"] == "result"
    )

    return result_data_assets


def get_latest_data_asset(
    data_assets: Sequence[DataAssetAPI],
) -> DataAssetAPI:
    return sorted(data_assets, key=lambda asset: asset["created"])[-1]


def get_session_sorted_data_asset(
    session: str | npc_session.SessionRecord,
) -> DataAssetAPI:
    """
    Examples:
        >>> asset = get_session_sorted_data_asset('ecephys_703333_2024-04-09_1')
        >>> asset = get_session_sorted_data_asset('668759_20230711')
        >>> assert isinstance(asset, dict)
    """
    session_result_data_assets = get_session_data_assets(session)
    sorted_data_assets = tuple(
        data_asset
        for data_asset in session_result_data_assets
        if is_sorted_data_asset(data_asset) and data_asset.get("files", -1) > 2
    )

    if not sorted_data_assets:
        raise ValueError(f"Session {session} has no sorted data assets")

    return get_latest_data_asset(sorted_data_assets)


@functools.cache
def get_sessions_with_data_assets(
    subject: str | int,
) -> tuple[npc_session.SessionRecord, ...]:
    """
    Examples:
        >>> sessions = get_sessions_with_data_assets(668759)
        >>> assert len(sessions) > 0
    """
    assets = get_subject_data_assets(subject)
    sessions = set()
    for asset in assets:
        try:
            session = npc_session.SessionRecord(asset["name"])
        except ValueError:
            continue
        sessions.add(session)
    return tuple(sessions)


def get_data_asset(asset: str | uuid.UUID | DataAssetAPI) -> DataAssetAPI:
    """Converts an asset uuid to dict of info from CodeOcean API."""
    if not isinstance(asset, Mapping):
        response = get_codeocean_client().get_data_asset(str(asset))
        response.raise_for_status()
        asset = response.json()
    assert isinstance(asset, Mapping), f"Unexpected {type(asset) = }, {asset = }"
    return asset


def is_raw_data_asset(asset: str | DataAssetAPI) -> bool:
    """
    Examples:
        >>> is_raw_data_asset('83636983-f80d-42d6-a075-09b60c6abd5e')
        True
        >>> is_raw_data_asset('173e2fdc-0ca3-4a4e-9886-b74207a91a9a')
        False
    """
    asset = get_data_asset(asset)
    if is_sorted_data_asset(asset):
        return False
    return asset.get("custom_metadata", {}).get(
        "data level"
    ) == "raw data" or "raw" in asset.get("tags", [])


def is_sorted_data_asset(asset: str | DataAssetAPI) -> bool:
    """
    Examples:
        >>> is_sorted_data_asset('173e2fdc-0ca3-4a4e-9886-b74207a91a9a')
        True
        >>> is_sorted_data_asset('83636983-f80d-42d6-a075-09b60c6abd5e')
        False
    """
    asset = get_data_asset(asset)
    if "ecephys" not in asset["name"]:
        return False
    return "sorted" in asset["name"]


def get_session_raw_data_asset(
    session: str | npc_session.SessionRecord,
) -> DataAssetAPI:
    """
    Examples:
        >>> get_session_raw_data_asset('668759_20230711')["id"]
        '83636983-f80d-42d6-a075-09b60c6abd5e'
    """
    session = npc_session.SessionRecord(session)
    raw_assets = tuple(
        asset for asset in get_session_data_assets(session) if is_raw_data_asset(asset)
    )

    if not raw_assets:
        raise ValueError(f"Session {session} has no raw data assets")

    return get_latest_data_asset(raw_assets)


def get_surface_channel_root(session: str | npc_session.SessionRecord) -> upath.UPath:
    """Reconstruct path to surface channel data in bucket (e.g. on s3) using data-asset
    info from Code Ocean.

    Examples:
        >>> get_surface_channel_root('660023_20230808')
        S3Path('s3://aind-ephys-data/ecephys_660023_2023-08-08_15-11-14')
        >>> assert get_surface_channel_root('660023_20230808') != get_raw_data_root('660023_20230808')
        >>> get_surface_channel_root('649943_20230216')
        Traceback (most recent call last):
        ...
        FileNotFoundError: 649943_20230216 has no surface channel data assets
    """
    raw_asset = get_surface_channel_raw_data_asset(session)
    return get_path_from_data_asset(raw_asset)


def get_surface_channel_raw_data_asset(
    session: str | npc_session.SessionRecord,
) -> DataAssetAPI:
    """For a main ephys session (implict idx=0), find a raw asset corresponding to
    the second session on the same day (idx=1).
    """
    session = npc_session.SessionRecord(session).with_idx(1)
    try:
        raw_assets = tuple(
            asset
            for asset in get_session_data_assets(session)
            if is_raw_data_asset(asset)
        )
    except SessionIndexError:
        raise FileNotFoundError(
            f"{session} has no surface channel data assets"
        ) from None
    return get_latest_data_asset(raw_assets)


@functools.cache
def get_codoecean_session_id(
    session: str | npc_session.SessionRecord,
) -> str:
    """Get the Code Ocean session ID for a given session, which includes session
    start time.

    Examples:
        >>> get_codoecean_session_id('703333_2024-04-09')
        'ecephys_703333_2024-04-09_13-06-44'
        >>> get_codoecean_session_id('703333_2024-04-09_1')
        'ecephys_703333_2024-04-09_15-14-46'
    """
    session = npc_session.SessionRecord(session)
    data_assets = [
        asset
        for asset in get_subject_data_assets(session.subject)
        if asset["name"].startswith(f"ecephys_{session.subject}_{session.date}")
    ]

    def parse_session_id(s: str) -> str:
        """
        >>> parse_session_id('ecephys_703333_2024-04-09_13-06-44_sorted_2024-04-12_12-12-12')
        'ecephys_703333_2024-04-09_13-06-44'
        """
        pattern: str = (
            f"^(?P<id>ecephys_{session.subject}_{session.date}_{npc_session.PARSE_TIME}).*"
        )
        if m := re.match(
            f"{pattern}",
            s,
        ):
            return m.group("id")
        raise ValueError(f"Could not extract session ID from {s!r}")

    asset_names = tuple(asset["name"] for asset in data_assets)
    session_times = sorted(
        {
            time
            for time in map(npc_session.extract_isoformat_time, asset_names)
            if time is not None
        }
    )
    session_times_to_assets = {
        session_time: tuple(
            asset
            for asset in data_assets
            if npc_session.extract_isoformat_time(asset["name"]) == session_time
        )
        for session_time in session_times
    }
    if not session_times_to_assets:
        raise ValueError(
            f"No assets found on codeocean for {session=} - cannot deduce session ID"
        )
    if len(session_times) < session.idx + 1:  # 0-indexed
        raise SessionIndexError(
            f"Number of assets is less than expected: cannot extract asset for session idx = {session.idx} from {asset_names = }"
        )
    session_assets = session_times_to_assets[session_times[session.idx]]
    session_id = parse_session_id(session_assets[0]["name"])
    assert all(
        parse_session_id(asset["name"]) == session_id for asset in session_assets
    )
    return session_id


@functools.cache
def get_raw_data_root(session: str | npc_session.SessionRecord) -> upath.UPath:
    """Reconstruct path to raw data in bucket (e.g. on s3) using data-asset
    info from Code Ocean.

        >>> get_raw_data_root('668759_20230711')
        S3Path('s3://aind-ephys-data/ecephys_668759_2023-07-11_13-07-32')
    """
    raw_asset = get_session_raw_data_asset(session)

    return get_path_from_data_asset(raw_asset)


def get_path_from_data_asset(asset: DataAssetAPI) -> upath.UPath:
    """Reconstruct path to raw data in bucket (e.g. on s3) using data asset
    uuid or dict of info from Code Ocean API."""
    if "source_bucket" not in asset:
        raise ValueError(
            f"Asset {asset['id']} has no `source_bucket` info - not sure how to create UPath:\n{asset!r}"
        )
    bucket_info = asset["source_bucket"]
    roots = {"aws": "s3", "gcs": "gs"}
    if bucket_info["origin"] not in roots:
        raise RuntimeError(
            f"Unknown bucket origin - not sure how to create UPath: {bucket_info = }"
        )
    return upath.UPath(
        f"{roots[bucket_info['origin']]}://{bucket_info['bucket']}/{bucket_info['prefix']}"
    )


def run_capsule_or_pipeline(
    data_assets: list[ComputationDataAsset], id: str, is_pipeline: bool = False
) -> CapsuleComputationAPI:
    if is_pipeline:
        run_capsule_request = RunCapsuleRequest(
            pipeline_id=id,
            data_assets=data_assets,
        )
    else:
        run_capsule_request = RunCapsuleRequest(
            capsule_id=id,
            data_assets=data_assets,
        )

    response = get_codeocean_client().run_capsule(run_capsule_request)
    response.raise_for_status()
    return response.json()


def get_session_capsule_pipeline_data_asset(
    session: str | npc_session.SessionRecord, process_name: str
) -> DataAssetAPI:
    """
    Returns the data asset for a given model
    >>> asset = get_session_capsule_pipeline_data_asset('676909_2023-12-13', 'dlc_eye')
    >>> asset = get_session_capsule_pipeline_data_asset('676909_2023-12-13', 'sorted')
    >>> asset['name']
    'ecephys_676909_2023-12-13_13-43-40_sorted_2024-03-01_16-02-45'
    """
    session = npc_session.SessionRecord(session)

    session_data_assets = get_session_data_assets(session)
    session_model_asset = tuple(
        asset for asset in session_data_assets if process_name in asset["name"]
    )
    if not session_model_asset:
        raise FileNotFoundError(f"{session} has no {process_name} results")

    return get_latest_data_asset(session_model_asset)


def create_session_data_asset(
    session: str | npc_session.SessionRecord, computation_id: str, data_asset_name: str
) -> requests.models.Response | None:
    session = npc_session.SessionRecord(session)

    if is_computation_errored(computation_id) or not is_computation_finished(
        computation_id
    ):
        return None

    source = aind_codeocean_requests.Source(
        computation=aind_codeocean_requests.Sources.Computation(id=computation_id)
    )
    tags = [str(session.subject), "derived", "ephys", "results"]
    custom_metadata = {
        "data level": "derived data",
        "experiment type": "ecephys",
        "modality": "Extracellular electrophysiology",
        "subject id": str(session.subject),
    }

    create_data_asset_request = aind_codeocean_requests.CreateDataAssetRequest(
        name=data_asset_name,
        mount=data_asset_name,
        tags=tags,
        source=source,
        custom_metadata=custom_metadata,
    )

    asset = get_codeocean_client().create_data_asset(create_data_asset_request)
    asset.raise_for_status()
    return asset


def set_asset_viewable_for_everyone(asset_id: str) -> None:
    response = get_codeocean_client().update_permissions(
        data_asset_id=asset_id, everyone="viewer"
    )
    response.raise_for_status()
    logger.debug(f"Asset {asset_id} made viewable for everyone")


def get_job_status(job_id: str, check_files: bool = False) -> CapsuleComputationAPI:
    """Current status from CodeOcean API, but with an additional check for no
    output files, which is a common error in the spike-sorting pipeline."""
    response = get_codeocean_client().get_computation(job_id)
    response.raise_for_status()
    job_status = response.json()
    if check_files and is_computation_errored(job_status):
        logger.info(f"Job {job_status['id']} errored, updating status")
        job_status["end_status"] = "failed"
    return job_status


def _parse_job_id_and_response(
    job_id_or_response: str | CapsuleComputationAPI,
) -> CapsuleComputationAPI:
    if isinstance(job_id_or_response, str):
        return get_job_status(job_id_or_response)
    return job_id_or_response


def is_computation_finished(job_id_or_response: str | CapsuleComputationAPI) -> bool:
    """
    >>> is_computation_finished(EXAMPLE_JOB_STATUS)
    True
    >>> is_computation_finished({"state": "initializing"})
    False
    >>> is_computation_finished({"state": "running"})
    False
    """
    job_status = _parse_job_id_and_response(job_id_or_response)
    return job_status["state"] == "completed"


def get_result_names(job_id: str) -> list[str]:
    """File and folder names in the output directory of a job's result"""
    available_results = (
        get_codeocean_client().get_list_result_items(job_id).json()["items"]
    )
    result_item_names = sorted(item["name"] for item in available_results)
    return result_item_names


def is_computation_errored(job_id_or_response: str | CapsuleComputationAPI) -> bool:
    """Job status may say `completed` but the pipeline still errored: check the
    output folder for indications of error.

    - no files (or only `nextflow` and `output` files for pipeline runs)
    - `end_status` == `failed`
    - `has_results` == False
    - `output` file contains `Out of memory.`

    >>> is_computation_errored(EXAMPLE_JOB_STATUS)
    False
    >>> is_computation_errored(EXAMPLE_JOB_STATUS | {"end_status": "failed"})
    True
    >>> is_computation_errored(EXAMPLE_JOB_STATUS | {"has_results": False})
    True
    >>> is_computation_errored(EXAMPLE_JOB_STATUS | {"id": "d5444fc9-9c0f-4c91-90c0-8d17969971b8"})
    True
    """
    job_status = _parse_job_id_and_response(job_id_or_response)
    if not is_computation_finished(job_status):
        return False
    job_id = job_status["id"]
    if "error" in job_status["state"]:
        return True
    if job_status.get("end_status", None) == "failed":
        return True
    if job_status["has_results"] is False:
        logger.debug(f"Job {job_id} suspected error based on no results")
        return True

    if job_status["state"] == "completed":
        # check if errored based on files in result
        result_item_names = get_result_names(job_id)
        is_no_files = len(result_item_names) == 0
        is_pipeline_error = len(result_item_names) == 2 and result_item_names == [
            "nextflow",
            "output",
        ]
        is_capsule_error = len(result_item_names) == 1 and result_item_names == [
            "output"
        ]
        if is_no_files or is_pipeline_error or is_capsule_error:
            logger.debug(
                f"Job {job_id} suspected error based on number of files available in result"
            )
            return True
        if "output" in result_item_names:
            output = requests.get(
                get_codeocean_client()
                .get_result_file_download_url(job_id, "output")
                .json()["url"]
            ).text
            if "Out of memory." in output:
                logger.debug(
                    f"Job {job_id} output file includes 'Out of memory.' in text"
                )
                return True
            if "Traceback (most recent call last)" in output:
                logger.debug(
                    f"Job {job_id} suspected error based on python traceback in output"
                )
                return True
            if "Command error:" in output:
                logger.debug(
                    f"Job {job_id} suspected error based on pipeline error message"
                )
                return True
            if "The CUDA error was:" in output:
                logger.warning(
                    f"Job {job_id} suspected failure based on CUDA error message"
                )
                # return True - currently (Apr 2024) this results from single
                # probes not sorting (due to artefacts or other issues), but other
                # probes still usable
            if all(
                text in output.lower()
                for text in ("sorting", "kilosort", "N E X T F L O W".lower())
            ):
                if "nwb" not in result_item_names:
                    logger.debug(
                        f"Job {job_id} suspected error based on missing NWB file"
                    )
                    return True
    return False


def get_skipped_probes(session_id: str | npc_session.SessionRecord) -> str:
    """Only works with new pipeline output

    Examples:
        >>> get_skipped_probes('702136_2024-03-05')
        'E'
        >>> get_skipped_probes('666986_2023-08-14')
        'B'
        >>> get_skipped_probes('668755_2023-08-28')
        ''
    """
    output = get_sorting_output_text(session_id)
    skipped_probes = ""
    if "skip" not in output.lower():
        return skipped_probes
    for text in output.split("Skipping further processing for this recording")[:-1]:
        preprocessing = text.split("Preprocessing".upper())[-1]
        skipped_probes += npc_session.ProbeRecord(preprocessing)
    return skipped_probes


def get_sorting_output_text(session_id: str | npc_session.SessionRecord) -> str:
    """Contents of the sorting pipeline `output` file (log)"""
    session = npc_session.SessionRecord(session_id)
    output_path = next(
        (p for p in s3.get_sorted_data_paths_from_s3(session) if p.name == "output"),
        None,
    )
    if output_path is None:
        raise FileNotFoundError(f"No output file found for {session}")
    return output_path.read_text()


if __name__ == "__main__":
    import doctest

    doctest.testmod(
        optionflags=(doctest.IGNORE_EXCEPTION_DETAIL | doctest.NORMALIZE_WHITESPACE)
    )
