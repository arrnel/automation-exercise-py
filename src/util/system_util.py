import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional, Literal, List


def get_tmp_screenshot_folder() -> str:
    """Returns absolute string path to file in tmp folder for screenshots"""
    root_path = Path(os.path.dirname(__file__)).parent
    return os.path.join(root_path, "resources", "tmp", "screenshots")


def get_path_in_resources(file_path: str) -> str:
    """
    Returns absolute string path to file in resources
    :param file_path: path to file in resources. Example: "files/file.txt"
    :return: Example: "/home/$USER/dev/python/automation_exercise/resources/files/file.txt"
    """
    root_path = Path(os.path.dirname(__file__)).parent.parent
    folders = file_path.split("/")
    return os.path.join(root_path, "resources", *folders)


def get_path_in_root(file_path: str) -> str:
    """
    Returns absolute string path to file in resources
    :param file_path: path to file in resources. Example: "env/.env.local"
    :return: Example: "/home/$USER/dev/python/automation_exercise/env/.env.local"
    """
    root_path = Path(os.path.dirname(__file__)).parent.parent
    folders = file_path.split("/")
    return os.path.join(root_path, *folders)


def get_allure_results_path() -> str:
    """
    Returns allure results path
    :return: Example: "/home/$USER/dev/python/automation_exercise/allure-results"
    """
    from src.config.config import CFG

    if CFG.is_remote():
        return "/allure-results"
    root_path = Path(os.path.dirname(__file__)).parent.parent
    return os.path.join(root_path, "allure-results")


def parse_file_name_in_path(path: str) -> str:
    return path.split("/")[-1]


def get_files_in_directory(
    path_to_dir: str,
    file_extensions: set[str] = frozenset(),
    starts_with: Optional[str] = None,
    order_by: Optional[Literal["name", "date_time"]] = None,
    order_direction: Optional[Literal["asc", "desc"]] = "asc",
) -> List[str]:

    files = []
    actual_file_names = os.listdir(path_to_dir)
    for file_name in actual_file_names:

        if starts_with and not file_name.startswith(starts_with):
            continue
        absolute_path = os.path.join(path_to_dir, file_name)
        is_file = os.path.isfile(absolute_path)
        is_file_matched = not file_extensions or (
            file_extensions
            and os.path.splitext(absolute_path)[1].lower() in file_extensions
        )
        if is_file and is_file_matched:
            files.append(absolute_path)

    if not order_by:
        return files

    reverse = order_direction.lower() == "desc"
    return sort_files(files, order_by=order_by, reverse=reverse)


def sort_files(files: List[str], order_by: str, reverse: bool) -> List[str]:
    if order_by == "name":
        files.sort(key=lambda path: os.path.basename(path).lower(), reverse=reverse)
    elif order_by == "date_time":
        files.sort(key=lambda path: os.path.getmtime(path), reverse=reverse)
    else:
        raise ValueError(
            f"Unsupported order_by value: {order_by}. Available values: 'name', 'date_time'"
        )
    return files


def save_as_file(abs_file_path: str, content: bytes) -> None:
    """
    Save content as a file (rewrites file if exists)
    :param abs_file_path: abs path to file from resources. Example: "files/file.txt"
    :param content: bytes to save
    """
    with open(abs_file_path, "wb") as file:
        file.write(content)


def save_in_file(abs_file_path: str, content) -> None:
    """
    Save content in a file (only append content into file)
    :param abs_file_path: abs path to file from resources. Example: "files/file.txt"
    :param content:
    :return:
    """
    with open(abs_file_path, "wb") as file:
        file.write(content)


def remove_from_resources(file_path: str) -> None:
    """
    Removes file from resources folder
    :param file_path: path to folder/file from resources. Example: "files/file.txt"
    """
    path_to_file = get_path_in_resources(file_path)
    if os.path.exists(path_to_file):
        os.remove(file_path)


def create_folder(abs_path_to_dir: str) -> None:
    """
    Creates folder in resources folder
    :param abs_path_to_dir: absolute path to folder. Example: "/home/selenium/Downloads"
    """
    path_to_dir = Path(abs_path_to_dir)
    if path_to_dir.exists() and path_to_dir.is_dir():
        return

    path_to_dir.mkdir(parents=True)


def create_folder_in_resources(relative_path_to_dir: str) -> None:
    """
    Creates folder in resources folder
    :param relative_path_to_dir: path to folder/file from resources. Example: "files/file.txt"
    """
    path_to_dir = get_path_in_resources(relative_path_to_dir)
    if not os.path.exists(path_to_dir):
        os.mkdir(path_to_dir)


def remove_all_items_from_folder(
    abs_path_to_dir: str, by_remove_folder: bool = True
) -> None:
    folder = Path(abs_path_to_dir)

    if not folder.exists():
        return

    if folder.is_file() or folder.is_symlink():
        raise ValueError(
            f"Invalid path to folder. Provided path is a file: {abs_path_to_dir}"
        )

    if by_remove_folder:
        shutil.rmtree(folder)
        folder.mkdir(parents=True, exist_ok=True)
    else:
        for item in folder.iterdir():
            try:
                if item.is_symlink() or item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            except FileNotFoundError:
                # File could be deleted
                continue


def execute_docker_container_command(
    container_id: str,
    *commands: str,
    timeout=None,
) -> str:
    print(f"Container id: {container_id}, commands: {commands}")
    return subprocess.run(
        [
            "docker",
            "exec",
            "-i",
            container_id,
            *commands,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
    ).stdout.strip()


def file_exists_in_docker_container(container_id: str, path_to_file: str) -> bool:
    return bool(
        int(
            execute_docker_container_command(
                container_id,
                "sh",
                "-c",
                f"[ -f {path_to_file} ] && echo 1 || echo 0",
                timeout=2,
            )
        )
    )
