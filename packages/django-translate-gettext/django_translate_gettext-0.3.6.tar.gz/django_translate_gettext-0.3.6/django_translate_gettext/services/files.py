import ast
from pathlib import Path

from django_translate_gettext.constants import TO_SKIP
from django_translate_gettext.services.transformers import ClassDefTransformer


def fetch_app_files(app_name: str) -> set[Path]:
    """Fetch all python files in the app directory excluding the files in the TO_SKIP list.

    Args:
        app_name (str): The app name to fetch the files from.

    Returns:
        set[Path]: set of filtered Pathlib objects for the files in the app.
    """
    return {
        file
        for file in Path(app_name).rglob("*.py")
        if file.is_file() and not any(skip in str(file) for skip in TO_SKIP)
    }


def update_py_file(*, file_path: Path) -> None:
    """Update the python file with the gettext call wrapping.

    Args:
        file_path (Path): The file path Pathlib object to update.

    Returns:
        None
    """
    tree = ast.parse(file_path.read_text())

    transformer = ClassDefTransformer()
    new_tree = transformer.visit(tree)
    new_tree = transformer.insert_getetxt_import(new_tree)

    code = ast.unparse(new_tree)
    file_path.write_text(code)
