""" test medi info and pymedia info loacally """

import os
import pathlib
import json
from pymediainfo import MediaInfo


def test_should_return_mediainfo():
    """test should return mediainfo"""
    # Arrange
    file_path = os.path.join(
        os.path.dirname(__file__), "samples/Video/BigBuckBunny.mp4"
    )
    # Act
    media_info = MediaInfo.parse(file_path)
    # Assert
    assert media_info is not None

    media_info_jason = json.dumps(media_info.to_json())
    assert media_info_jason is not None
    with open(
        os.path.join(os.path.dirname(__file__), "samples/Video/BigBuckBunny.mp4.json"),
        "w",
        encoding="utf-8",
    ) as file:
        file.write(media_info.to_json())


def test_json_extract_all_files():
    """should extract media info in json format for all files in each folder
    but only if json file is missing or if the file is newer than the json file
    """
    # Arrange
    root_dir = os.path.join(os.path.dirname(__file__), "samples")
    # Act
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            json_file_path = file_path + ".json"
            if os.path.splitext(file_path)[1] == ".json":
                continue
            if os.path.exists(json_file_path):
                if os.path.getmtime(json_file_path) > os.path.getmtime(file_path):
                    continue
            media_info = MediaInfo.parse(file_path)
            assert media_info is not None
            with open(json_file_path, "w", encoding="utf-8") as file:
                file.write(media_info.to_json())