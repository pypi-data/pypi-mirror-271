import os
import re
from datetime import datetime, timedelta
from typing import Dict, Union
from urllib.parse import quote, unquote

from botocore.exceptions import ClientError
from gable.helpers.data_asset_s3.logger import log_debug, log_error, log_trace
from gable.helpers.data_asset_s3.path_pattern_manager import (
    DATE_PLACEHOLDER_TO_REGEX,
    DAY_REGEX,
    HOUR_REGEX,
    MONTH_REGEX,
    YEAR_REGEX,
    PathPatternManager,
)
from gable.helpers.logging import log_execution_time


@log_execution_time
def discover_patterns_from_s3_bucket(
    client, bucket_name: str, files_per_directory: int = 1000, **kwargs
) -> Dict[str, set[str]]:
    """
    Discover patterns in an S3 bucket.

    Args:
        bucket (str): S3 bucket.
        files_per_directory (int, optional): Number of files per directory. Defaults to 1000.
        **kwargs:
            include: list of prefixes to include. (TODO: change to be pattern instead of just prefix)
            TODO: add exclude as well
            lookback_days: int, number of days to look back from the latest day in the list of paths. For example
                if the latest path is 2024/01/02, and lookback_days is 4, then the paths return will have
                2024/01/02, 2024/01/01, 2023/12/31, and 2023/12/30
    Returns:
        list[str]: List of patterns.
    """
    log_trace("Starting pattern discovery in bucket: {}", bucket_name)
    try:
        files = [
            file["Key"]
            for file in _list_files(
                client,
                bucket_name,
                files_per_directory,
                "",
                trim_recent_patterns=True,
                **kwargs,
            )
        ]
        patterns = _discover_patterns_from_filepaths(files)
        log_trace("Completed pattern discovery in bucket: {}", bucket_name)
        return patterns
    except Exception as e:
        log_error("Failed during pattern discovery in {}: {}", bucket_name, str(e))
        raise


@log_execution_time
def discover_filepaths_from_patterns(
    client, bucket_name: str, patterns: list[str], file_count: int = 1000, **kwargs
) -> list[str]:
    """
    Discover filepaths in an S3 bucket from patterns.

    Args:
        bucket_name (str): S3 bucket.
        patterns (list[str]): List of patterns.

    Returns:
        list[str]: List of filepaths.
    """
    log_trace("Starting filepath discovery from patterns in {}", bucket_name)
    filepaths: set[str] = set()
    for pattern in patterns:
        log_trace("Discovering filepaths for pattern: {}", pattern)
        for filepath in _get_latest_filepaths_from_pattern(
            client, bucket_name, pattern, file_count, **kwargs
        ):
            filepaths.add(filepath)
    log_trace("Completed filepath discovery from patterns in {}", bucket_name)
    return list(filepaths)


@log_execution_time
def _get_latest_filepaths_from_pattern(
    client, bucket_name: str, pattern: str, file_count: int, **kwargs
) -> list[str]:
    """
    Get the n latest files from a DARN pattern.

    Args:
        bucket_name (str): S3 bucket.
        pattern (str): pattern.
        count (int): Number of files to get.

    Returns:
        list[str]: list of filepaths
    """
    optimized_prefix = _generate_optimized_prefix(pattern)
    files = _list_files(client, bucket_name, file_count, optimized_prefix, **kwargs)
    files = sorted(files, key=lambda x: x["LastModified"], reverse=True)
    return [file["Key"] for file in files[:file_count]]


def _generate_optimized_prefix(pattern: str) -> str:
    optimized_prefix_parts = []
    now = datetime.now()
    regex_replacements = [
        (r"{YYYY}", now.strftime("%Y")),
        (r"{MM}", now.strftime("%m")),
        (r"{DD}", now.strftime("%d")),
        (r"{YYYY-MM-DD}", now.strftime("%Y-%m-%d")),
        (r"{YYYY-MM-DD.+}.*", now.strftime("%Y-%m-%d")),
        (r"{YYYYMMDD}", now.strftime("%Y%m%d")),
        (r"{YYYYMMDD.+}.*", now.strftime("%Y%m%d")),
    ]
    for part in pattern.split("/"):
        found_match = False
        cannot_optimize_further = False
        for regex, replacement in regex_replacements:
            if re.match(".*" + regex, part):
                found_match = True
                replacement_part = re.sub(regex, replacement, part)
                optimized_prefix_parts.append(replacement_part)
                cannot_optimize_further = regex.endswith(".*")
                break
        if not found_match:
            if "{" in part:  # no match found, so we can't optimize any further
                break
            else:
                optimized_prefix_parts.append(part)
        elif cannot_optimize_further:
            break
    return "/".join(optimized_prefix_parts)


def _discover_patterns_from_filepaths(
    filepaths: list[str],
) -> Dict[str, set[str]]:
    """
    Discover patterns in a list of filepaths.

    Args:
        filepaths (list[str]): List of filepaths.

    Returns:
        Iterable[str]: List of patterns.
    """
    log_trace("Adding filepaths to PathPatternManager")
    path_manager = PathPatternManager()
    path_manager.add_filepaths(filepaths)
    return path_manager.get_pattern_to_actual_paths()


def _list_files(
    client, bucket_name: str, files_per_directory: int, prefix: str, **kwargs
) -> list[dict]:
    """
    List objects in an S3 bucket.

    Args:
        bucket_name (str): S3 bucket.
        files_per_directory: (int, optional): Number of files per directory. Defaults to all files
        prefix (str): Prefix. For all files, supply an empty string.
        **kwargs:
            include: list of prefixes to include. (TODO: change to be pattern instead just prefix)
            TODO: add exclude as well
            lookback_days: int, number of days to look back for recent patterns.
    Returns:
        list[dict]: mapping of file names to contents.
    """
    _validate_bucket_exists(client, bucket_name)
    try:
        log_debug("Listing files in {}: prefix={}", bucket_name, prefix)
        dirpaths = _list_all_dirpaths(client, bucket_name, prefix, **kwargs)
        log_trace("Listed directories to crawl: {}", dirpaths)
        files: list[dict[str, dict]] = []
        for dirpath in dirpaths:
            files.extend(
                _list_all_files_paginated(
                    client,
                    bucket_name,
                    files_per_directory,
                    dirpath,
                )
            )
        log_debug("Listed files in {}: prefix={}", bucket_name, prefix)
        return files
    except Exception as e:
        log_error("Failed to list files in {}: {}", bucket_name, str(e))
        return []


def _list_all_files_paginated(
    client, bucket_name: str, max_files: int, prefix: str = ""
) -> list[dict[str, dict]]:
    """
    List objects in an S3 bucket.

    Args:
        bucket_name (str): S3 bucket.
        max_files (int): Maximum number of files to list.
        prefix (str, optional): Prefix. Defaults to None.
    Returns:
        dict[str, object]: mapping of file names to contents.
    """
    log_trace(
        "Starting to paginate files in bucket: {} with prefix: {}", bucket_name, prefix
    )
    paginator = client.get_paginator("list_objects_v2")
    files: list[dict[str, dict]] = []
    for page in paginator.paginate(
        Bucket=bucket_name,
        Prefix=prefix,
        PaginationConfig={"MaxItems": max_files},
    ):
        for obj in page.get("Contents", []):
            files.append(obj)
    log_trace("Completed listing files, total files gathered: {}", len(files))
    return files


def _list_all_dirpaths(client, bucket_name: str, prefix: str, **kwargs) -> list[str]:
    """
    List all directories in an S3 bucket.

    Args:
        bucket_name (str): S3 bucket.
        prefix (str): Prefix. This is used for recursive calls and differs from kwargs["include"] which is a configuration option.
        **kwargs:
            include: list of prefixes to include. (TODO: change to be pattern instead just prefix)
            trim_recent_patterns: bool, whether to optimize the selection of directories to list.
            TODO: add exclude as well
            lookback_days: int, number of days to look back for recent patterns.
    Returns:
        list[str]: List of directories.
    """
    include: list[str] = kwargs.get("include", None)
    lookback_days: int = kwargs.get("lookback_days", 0)
    include = [] if include is None or include == "" else include
    if len(include) > 0 and not any(
        [prefix.startswith(incl) or incl.startswith(prefix) for incl in include]
    ):
        return []

    trim_recent_patterns = kwargs.get("trim_recent_patterns", False)
    paginator = client.get_paginator("list_objects_v2")
    pagination_result = paginator.paginate(
        Bucket=bucket_name, Delimiter="/", Prefix=prefix
    )
    search_result = _extract_prefixes_from_results(
        pagination_result.search("CommonPrefixes") or []
    )
    content_result = pagination_result.search("Contents")
    dirpaths = []
    log_trace("Listing dirpaths for prefix: {}", prefix)
    prefix_in_include = (
        len(include) > 0 and any([incl in prefix for incl in include])
    ) or len(include) == 0
    file_exists = next(content_result, None) is not None
    if prefix_in_include and file_exists:
        # if the prefix is in the include list, and there are files at the prefix location, then the prefix is a dirpath
        dirpaths.append(prefix)

    common_prefixes = (
        _trim_recent_patterns(search_result, include, lookback_days)
        if trim_recent_patterns
        else search_result
    )
    for next_prefix in common_prefixes:
        if next_prefix is None:
            # once next_prefix is none, we've hit the bottom of the dir tree, so the current prefix arg is a full prefix
            if prefix not in dirpaths:
                # multiple paginations can return the same prefix, so avoid duplication
                dirpaths.append(prefix)
        else:
            dirpaths.extend(
                _list_all_dirpaths(client, bucket_name, next_prefix, **kwargs)
            )
    log_trace(
        "Completed directory listing under prefix {}, total directories found: {}",
        prefix,
        len(dirpaths),
    )
    return dirpaths


def _extract_prefixes_from_results(
    results: list[Union[dict, None]]
) -> list[Union[str, None]]:
    return [(result or {}).get("Prefix", None) for result in results]


def _strip_slashes(path: str) -> str:
    return path.strip("/")


def _trim_recent_patterns(
    paths: list[Union[str, None]], include: list[str], lookback_days: int
) -> list[Union[str, None]]:
    """
    Trim recent patterns from a list of paths in order to get a reduced set of paths for optimization.
    lookback_days is used to determine how many days back to look, from the latest day in the list of paths. For example
    if the latest path is 2024/01/02, and lookback_days is 4, then the paths return will have
    2024/01/02, 2024/01/01, 2023/12/31, and 2023/12/30
    """
    prefixes = set(
        [
            os.path.join("", *_strip_slashes(path or "").split("/")[:-1])
            for path in paths
        ]
    )
    if len(prefixes) == 0:
        return []
    if len(prefixes) > 1:
        raise ValueError(
            "Optimization does not make sense for multiple prefixes, they should be separate calls to this function"
        )

    suffixes = [
        None if path is None else _strip_slashes(path).split("/")[-1] for path in paths
    ]
    prefix = next(iter(prefixes))
    result_suffixes: list[Union[str, None]] = []
    max_num_type = None
    max_num, original_max_num_str = None, None
    max_date, original_max_date_format = None, None
    suffix_to_quote_count = {}
    for suffix in suffixes:
        proposed_path = os.path.join(prefix, suffix or "")
        if len(include) > 0 and any(
            [incl.startswith(proposed_path) for incl in include]
        ):
            result_suffixes.append(suffix)
        elif suffix:
            if re.match(
                rf".*/({YEAR_REGEX})/({MONTH_REGEX})/({DAY_REGEX})/?$", prefix
            ) and re.match(HOUR_REGEX, suffix):
                max_num_type = "hour"
            elif re.match(
                rf".*/({YEAR_REGEX})/({MONTH_REGEX})/?$", prefix
            ) and re.match(DAY_REGEX, suffix):
                max_num_type = "day"

            if len(suffix) <= 4 and suffix.isdigit():
                num = int(suffix)
                if max_num is None or num > max_num:
                    max_num = num
                    original_max_num_str = suffix
                else:
                    result_suffixes.append(None)
            else:
                found_match = False
                for reg, format in [
                    # return same order as in DATE_PLACEHOLDER_TO_REGEX
                    (DATE_PLACEHOLDER_TO_REGEX["{YYYY-MM-DD:HH:mm}"], "%Y-%m-%d:%H:%M"),
                    (DATE_PLACEHOLDER_TO_REGEX["{YYYYMMDD:HH:mm}"], "%Y%m%d:%H:%M"),
                    (DATE_PLACEHOLDER_TO_REGEX["{YYYY-MM-DD:HH}"], "%Y-%m-%d:%H"),
                    (DATE_PLACEHOLDER_TO_REGEX["{YYYYMMDD_HH}"], "%Y%m%d_%H"),
                    (DATE_PLACEHOLDER_TO_REGEX["{YYYYMMDD:HH}"], "%Y%m%d:%H"),
                    (DATE_PLACEHOLDER_TO_REGEX["{YYYYMMDDHH}"], "%Y%m%d%H"),
                    (DATE_PLACEHOLDER_TO_REGEX["{YYYY-MM-DD}"], "%Y-%m-%d"),
                    (DATE_PLACEHOLDER_TO_REGEX["{YYYYMMDD}"], "%Y%m%d"),
                ]:
                    decoded = suffix
                    quote_count = 0
                    while decoded != (decoded := unquote(decoded)):
                        quote_count += 1
                    suffix_to_quote_count[decoded] = quote_count
                    if re.match(reg, decoded):
                        try:
                            date = datetime.strptime(decoded, format)
                            if max_date is None or date > max_date:
                                max_date = date
                                original_max_date_format = format
                                found_match = True
                                break
                        except ValueError as e:
                            log_error(
                                "Failed to parse date with {}: {}", format, str(e)
                            )
                if not found_match:
                    result_suffixes.append(suffix)
        else:
            result_suffixes.append(None)

    extra_paths = []
    if max_num is not None:
        if max_num_type == "hour":
            if matches := re.match(
                rf".*/({YEAR_REGEX})/({MONTH_REGEX})/({DAY_REGEX})/?$", prefix
            ):
                year, month, day = matches.groups()
                latest_datetime = datetime(int(year), int(month), int(day), max_num)
                for day in range(lookback_days + 1):
                    for hour in range(24):
                        assembled_datetime = latest_datetime - timedelta(
                            days=day, hours=hour
                        )
                        extra_paths.append(
                            re.sub(
                                rf"/({YEAR_REGEX})/({MONTH_REGEX})/({DAY_REGEX})",
                                f"/{assembled_datetime.year:04d}/{assembled_datetime.month:02d}/{assembled_datetime.day:02d}",
                                prefix,
                            )
                            + f"/{assembled_datetime.hour:02d}/"
                        )
        elif max_num_type == "day":
            if matches := re.match(f".*/({YEAR_REGEX})/({MONTH_REGEX})/?$", prefix):
                year, month = matches.groups()
                latest_datetime = datetime(int(year), int(month), max_num)
                for days in range(lookback_days + 1):
                    assembled_datetime = latest_datetime - timedelta(days=days)
                    # there's no guarantee that these paths exist from the listing, but if they don't exist they just won't be read and parsed
                    extra_paths.append(
                        re.sub(
                            rf"/({YEAR_REGEX})/({MONTH_REGEX})",
                            f"/{assembled_datetime.year:04d}/{assembled_datetime.month:02d}",
                            prefix,
                        )
                        + f"/{assembled_datetime.day:02d}/"
                    )
        else:
            result_suffixes.append(original_max_num_str)
    if max_date is not None and original_max_date_format is not None:
        for day in range(lookback_days + 1):
            if "%M" in original_max_date_format:
                # fill in down to minute granularity
                for hour in range(24):
                    for minute in range(60):
                        result_suffixes.append(
                            (
                                max_date
                                - timedelta(days=day, hours=hour, minutes=minute)
                            ).strftime(original_max_date_format)
                        )
            elif "%H" in original_max_date_format:
                # fill in down to hour granularity
                for hour in range(24):
                    result_suffixes.append(
                        (max_date - timedelta(days=day, hours=hour)).strftime(
                            original_max_date_format
                        )
                    )
            else:  # just day granularity
                result_suffixes.append(
                    (max_date - timedelta(days=day)).strftime(original_max_date_format)
                )

    return [
        (
            None
            if suffix is None
            else os.path.join(
                prefix, _quote_n_times(suffix, suffix_to_quote_count.get(suffix, 0))
            )
            + "/"
        )
        for suffix in result_suffixes
    ] + extra_paths


def _quote_n_times(s: str, n: int) -> str:
    for _ in range(n):
        s = quote(s)
    return s


def _validate_bucket_exists(client, bucket_name: str) -> None:
    log_trace("Validating existence of bucket: {}", bucket_name)
    try:
        client.head_bucket(Bucket=bucket_name)
        log_trace("Bucket exists: {}", bucket_name)
    except Exception as e:
        if isinstance(e, ClientError):
            error_code = int(e.response["Error"]["Code"])
            if error_code == 404:
                print(f"Bucket {bucket_name} does not exist.")
                log_error("Bucket does not exist for {}: {}", bucket_name, str(e))
            elif error_code == 403:
                print(f"Access to bucket {bucket_name} is forbidden.")
                log_error(
                    "Access to bucket is forbidden for {}: {}", bucket_name, str(e)
                )
        raise ValueError(
            f"Bucket {bucket_name} does not exist or is not accessible. Check that AWS credentials are set up correctly."
        )


def replace_date_placeholders(pattern: str, date_str: str = "") -> str:
    """
    Replace date placeholders in the pattern with the provided date string or today's date if not provided.

    Args:
        pattern (str): The pattern containing placeholders.
        date_str (str, optional): Date in 'YYYY-MM-DD' format to inject into the pattern. Defaults to today's date.

    Returns:
        str: The pattern with date placeholders replaced.
    """
    # Use the current date if no date string is provided
    if date_str == "":
        date = datetime.now()
    else:
        date = datetime.strptime(date_str, "%Y-%m-%d")

    date = datetime.strptime(date_str, "%Y-%m-%d")
    year = date.strftime("%Y")
    month = date.strftime("%m")
    day = date.strftime("%d")

    # Replace the placeholders within the curly braces
    pattern = (
        pattern.replace("{YYYY}", year).replace("{MM}", month).replace("{DD}", day)
    )
    pattern = pattern.replace("{YYYY-MM-DD}", f"{year}-{month}-{day}")

    # Replace placeholders without curly braces if directly included in the string
    pattern = pattern.replace("{YYYYMMDD}", f"{year}{month}{day}")
    pattern = pattern.replace("YYYY", year).replace("MM", month).replace("DD", day)

    return pattern
