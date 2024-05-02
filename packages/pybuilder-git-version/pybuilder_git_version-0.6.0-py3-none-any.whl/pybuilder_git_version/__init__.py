from git import Repo
from git.exc import InvalidGitRepositoryError
from pybuilder.core import init, Project, Logger, before

from pybuilder_git_version.util import NoValidTagFoundError, find_latest_version


@init
def init_pybuilder_git_version(project: Project, logger: Logger):
    project.set_property_if_unset("use_git_version", True)
    project.set_property_if_unset("git_version_commit_distance_as_build_number", True)
    project.set_property_if_unset("git_version_master_branch", "master")


@before("prepare", only_once=True)
def update_version(project: Project, logger: Logger):
    logger.info("Using master branch %s", project.get_property("git_version_master_branch"))
    if project.get_property("use_git_version"):
        try:
            repo = Repo(project.basedir)
            latest_tag = find_latest_version(repo, logger, master_branch_name=project.get_property("git_version_master_branch"))
            project.version = latest_tag
            project.set_property("dir_dist", f"$dir_target/dist/{project.name}-{project.version}")
            logger.info("Set project version to %s", project.version)
        except InvalidGitRepositoryError:
            logger.warn("No git repository found")
        except NoValidTagFoundError:
            logger.warn("No git tags found")
    else:
        logger.info("Not using git version, disabled")
