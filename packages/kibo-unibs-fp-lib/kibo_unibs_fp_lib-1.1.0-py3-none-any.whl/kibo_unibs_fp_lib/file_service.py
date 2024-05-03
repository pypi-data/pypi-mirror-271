"""Module representing the FileService class"""

# Standard Libraries
import pickle

# Internal Libraries
from kibo_unibs_fp_lib.ansi_colors import RESET, AnsiFontColors, AnsiFontWeights


class FileService:
    """
    This class has useful methods to serialize/deserialize objects and save/load them to/from a
    file.
    """

    _CONSTRUCTOR_ERROR: str = "This class is not instantiable!"

    _RED_ERROR = f"\n{AnsiFontColors.RED}{AnsiFontWeights.BOLD}Error!{RESET}"
    _FILE_NOT_FOUND_ERROR = "Can't find the file %s\n"
    _READING_ERROR = "Problem reading the file %s\n"
    _WRITING_ERROR = "Problem writing the file %s\n"

    def __init__(self) -> None:
        """Prevents instantiation of this class

        Raises
        ------
        - NotImplementedError
        """

        raise NotImplementedError(FileService._CONSTRUCTOR_ERROR)

    @staticmethod
    def serialize_object(file_path: str, to_save: object) -> None:
        """Serialize to file whatever object is given.

        Params
        ------
        - file_path -> The file path where to save the serialized object.
        - to_save -> The object to serialize and save.
        """

        try:
            with open(file_path, "wb") as f:
                pickle.dump(to_save, f)
        except IOError:
            print(FileService._RED_ERROR)
            print(FileService._WRITING_ERROR % file_path)

    @staticmethod
    def deserialize_object(file_path: str) -> object:
        """Deserialize whatever object is saved in the given file.

        Params
        ------
        - file_path -> The file path where to find the serialized object.

        Returns
        -------
        An instance of the deserialized object.
        """

        try:
            with open(file_path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            print(FileService._RED_ERROR)
            print(FileService._FILE_NOT_FOUND_ERROR % file_path)
        except (IOError, pickle.UnpicklingError):
            print(FileService._RED_ERROR)
            print(FileService._READING_ERROR % file_path)

        return None
