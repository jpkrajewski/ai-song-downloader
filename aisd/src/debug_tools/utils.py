import json
import os

YOUTUBE_REQUEST_SUCCESS_LOG = "INFO - Request successful for:"
DATA_EXTRACTION_FAILURE_LOG = "ERROR - Failed to extract video URL: 'NoneType' object has no attribute 'get' from:"


def read_lines_from_file(file_path: str):
    """
    Reads a large file line by line and yields each line.

    This function is a generator, so it can handle large files without loading the entire content into memory.

    Args:
        file_path (str): The path to the log file that needs to be read.

    Yields:
        str: A line from the file, with extra whitespace or newlines stripped.
    """
    with open(file_path, "r") as file:
        for line in file:
            yield line.strip()  # `strip()` removes leading/trailing whitespace


def extract_search_query_from_log_line(line: str) -> str:
    """
    Extracts and formats the search query from a log line that contains a YouTube request.

    The search query is extracted from the URL in the log, and special characters like "+" are replaced by underscores.

    Args:
        line (str): A line of the log that contains the YouTube request URL.

    Returns:
        str: The formatted search query extracted from the log line.
    """
    return (
        line.split(YOUTUBE_REQUEST_SUCCESS_LOG, 1)[
            1
        ]  # Split the string at the first occurrence of YOUTUBE_REQUEST_SUCCESS_LOG
        .strip()  # Remove any extra whitespace
        .replace(
            "https://www.youtube.com/results?search_query=", ""
        )  # Remove the URL part
        .replace(
            "+", "_"
        )  # Replace '+' with underscores to create a more readable filename
    )


def extract_failed_json_data_and_save_to_files(log_file_path: str, target_dir: str):
    """
    Processes a log file to find entries where YouTube video URLs failed to be extracted,
    then saves the corresponding JSON data to separate files in the target directory.

    The function handles cases where JSON decoding fails, logging the error and continuing without crashing.

    Args:
        log_file_path (str): The path to the log file that contains the log entries.
        target_dir (str): The directory where the failed JSON data will be saved as individual files.

    Notes:
        This function will create the target directory if it does not exist.
    """
    os.makedirs(target_dir, exist_ok=True)  # Ensure the target directory exists

    current_youtube_query = ""  # Store the current search query for later use

    for i, line in enumerate(
        read_lines_from_file(log_file_path)
    ):  # Iterate over each line in the log file
        if YOUTUBE_REQUEST_SUCCESS_LOG in line:
            current_youtube_query = extract_search_query_from_log_line(
                line
            )  # Extract the search query
        elif DATA_EXTRACTION_FAILURE_LOG in line:
            try:
                # Try to extract and parse the JSON data from the error log line
                json_data = line.split("from:", 1)[
                    1
                ].strip()  # Extract the part after 'from:'
                json_data = json.loads(json_data)  # Parse the JSON string

                # Generate the file path for the failed JSON data
                failed_file_path = os.path.join(
                    target_dir, f"{current_youtube_query}_failed_entry_{i}.json"
                )

                # Write the JSON data to the file
                with open(failed_file_path, "w") as failed_file:
                    json.dump(json_data, failed_file)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON payload: {e}")
                # If there is a JSONDecodeError, skip saving this entry and continue with the next line
                pass
