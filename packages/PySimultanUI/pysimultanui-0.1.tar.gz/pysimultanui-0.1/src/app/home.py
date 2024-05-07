
from .. import core
from ..core.project_manager import ProjectManager

from ..core import method_mapper


def content() -> None:
    project_manager = ProjectManager()
    core.project_manager = project_manager
    # core.project_manager.geometry_file_manager = project_manager.geometry_file_manager
    core.project_manager.ui_content()
    # core.asset_manager.ui_content()
