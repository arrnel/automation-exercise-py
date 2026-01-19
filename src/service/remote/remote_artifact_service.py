from abc import ABCMeta, abstractmethod


class RemoteArtifactsService(metaclass=ABCMeta):

    @abstractmethod
    def get_file(
        self,
        session_id: str,
        file_name: str,
        retries: int = 5,
        delay: float = 1.0,
    ) -> bytes:
        """
        Delete file from current test container
        Args:
            session_id (str): browser session id.
            file_name (str): title of expected file. Example, "file.txt"
            retries (int): number of retries to get video
            delay (float): timeout before new retry
        """

    @abstractmethod
    def delete_file(self, session_id: str, file_name: str) -> None:
        """
        Delete file from current test container
        Args:
            session_id (str): browser session id.
            file_name (str): title of expected file. Example, "file.txt"
        """

    @abstractmethod
    def get_video(
        self,
        video_id: str,
        retries: int = 5,
        delay: float = 2.0,
    ) -> bytes:
        """
        Download a video from remote host
        Args:
            video_id (str): video id - test_title or session_id
            retries (int): number of retries to get video
            delay (float): timeout before new retry
        """
