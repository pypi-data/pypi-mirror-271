from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Generator

from nudenet import NudeDetector  # type:ignore

from ultima_scraper_detector.gui import Gui


class UltimaScraperDetector:
    def __init__(self, gui: bool = False):
        """
        Initializes an UltimaDetector instance.

        Args:
            gui (bool): Indicates whether a graphical user interface (GUI) should be used for displaying results.
        """
        self.nude_detector = NudeDetector()
        self.detections: dict[str, list[dict[str, Any]]] = {}
        self.gui = Gui() if gui else None

    def activate_gui(self):
        self.gui = Gui()
        return True

    def _detect(
        self,
        filepath: Path,
    ):
        filepath_string = filepath.as_posix()
        media_detections: list[dict[str, Any]] = []
        try:
            media_detections.extend(
                self.nude_detector.detect(  # type:ignore
                    filepath_string
                )
            )
            self.detections[filepath.name] = media_detections
        except AttributeError as _e:
            return media_detections, filepath
        return media_detections, filepath

    def detect(
        self,
        filepaths: list[Path] | Generator[Path, None, None],
        watch_keywords: list[str] = [],
    ):
        """
        Detects and analyzes media content for explicit content using a nude detection module.

        Args:
            filepaths (list[Path] | Generator[Path, None, None]): A list of paths to the media files to be analyzed.
            watch_keywords (list[str]): A list of keywords to watch for in the detected content.

        Returns:
            Dict[str, List[Dict[str, Any]]]: A dictionary mapping file names to lists of dictionaries representing
            detected media content. Each dictionary contains information such as class and confidence level.

        """

        def run_io_tasks_in_parallel(tasks: list[Path] | Generator[Path, None, None]):
            with ThreadPoolExecutor() as executor:
                running_tasks = [executor.submit(self._detect, task) for task in tasks]
                media_detections_collection: dict[str, list[dict[str, Any]]] = {}
                for running_task in running_tasks:
                    media_detections, filepath = running_task.result()
                    if self.gui:
                        # TKinter currently blocks main loop, maybe put it in another thread and give it a Queue
                        if watch_keywords:
                            has_keywords = all(
                                any(
                                    keyword.lower() in item["class"].lower()
                                    for item in media_detections
                                )
                                for keyword in watch_keywords
                            )

                            if has_keywords:
                                self.gui.update_image(filepath, media_detections)
                        else:
                            self.gui.update_image(filepath, media_detections)
                    media_detections_collection[filepath.name] = media_detections
                return media_detections_collection

        filepaths = [x for x in filepaths]
        media_detections_collection = run_io_tasks_in_parallel(filepaths)
        return media_detections_collection

    def predict_sex(self):
        """
        Predicts the overall gender based on the detected classes in media content.

        Returns:
            str: The predicted overall gender, which can be "MALE," "FEMALE," or "UNKNOWN."
        """
        detections = self.detections.values()
        # Count the occurrences of female-related classes and male-related classes
        male_detections = [
            detection
            for detections_list in detections
            for detection in detections_list
            if "MALE" in detection["class"] and "FEMALE" not in detection["class"]
        ]
        female_detections = [
            detection
            for detections_list in detections
            for detection in detections_list
            if "FEMALE" in detection["class"]
        ]

        male_count = len(male_detections)
        female_count = len(female_detections)

        # Determine overall gender based on the counts
        if female_count > male_count:
            overall_gender = "FEMALE"
        elif male_count > female_count:
            overall_gender = "MALE"
        else:
            overall_gender = "UNKNOWN"
        return overall_gender

    def reset_detections(self):
        """
        Clears the 'detections' list, resetting it for new data.

        Usage:
        >>> instance = UltimaScraperDetector()
        >>> instance.reset_detections()
        """
        self.detections.clear()
