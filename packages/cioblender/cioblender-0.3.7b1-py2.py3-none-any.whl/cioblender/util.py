from ciopath.gpath_list import PathList, GLOBBABLE_REGEX
# from ciopath.gpath import Path

from pathlib import Path as MyPath


def clean_path_pathlist(path):
    """Clean the path"""
    # convert the path to a PathList
    path = path.replace("\\", "/")
    path_list = PathList()
    path_list.add(path)
    # get the first path in the list
    cleaned_path = [p.fslash() for p in path_list][0]
    if ":" in cleaned_path:
        cleaned_path = cleaned_path.split(":")[1]
    cleaned_path = cleaned_path.replace("\\", "/")
    return cleaned_path

def clean_path(current_path):
    """Clean the path"""
    cleaned_path = current_path.replace("\\", "/")
    return cleaned_path


def clean_and_strip_path(current_path):
    """Clean the path"""
    cleaned_path = current_path
    # convert the path to a PathList
    try:
        if current_path:
            current_path = current_path.replace("\\", "/")
            current_path = MyPath(current_path).resolve(strict=True)
            current_path = str(current_path)
            # current_path = Path(current_path).fslash(with_drive=False)
            if ":" in current_path:
                current_path = current_path.split(":")[1]
            cleaned_path = current_path.replace("\\", "/")
            # print("cleaned_path: ", cleaned_path)
    except Exception as e:
        print("Unable to clean and strip path: {} error: {}", current_path, e)
    return cleaned_path

def resolve_path(filepath):
    try:
        filepath = MyPath(filepath).resolve(strict=True)
        filepath = str(filepath)
        filepath = filepath.replace("\\", "/")
    except Exception as e:
        print("Unable to resolve path: {} error: {}", filepath, e)
    return filepath
