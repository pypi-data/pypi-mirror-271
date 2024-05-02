import re

import semver
from git import Repo
from pybuilder.core import Logger


class NoValidTagFoundError(Exception):
    pass


def find_latest_version(repo: Repo, logger: Logger, master_branch_name: str = 'master') -> str:
    # valid_tags = [t for t in repo.tags if semver.VersionInfo.isvalid(t.name)]
    # logger.debug("Valid tags are: %s", [t.name for t in valid_tags])
    latest_tag, distance, branch_name = find_latest_tag_in_path(repo, logger)
    detached_head = branch_name is None
    logger.debug("latest tag = %s, distance = %s, branch_name = %s, master_branch_name = %s", latest_tag, distance, branch_name, master_branch_name)
    on_master_branch = not detached_head and branch_name == master_branch_name
    repo_dirty = repo.is_dirty()
    if distance == 0 and (on_master_branch or detached_head) and not repo_dirty:
        logger.info("Using unmodified tag %s", latest_tag)
        return latest_tag.name
    else:
        logger.debug("Bumping patch and adding build")
        current_version = semver.VersionInfo.parse(latest_tag.name)
        build_token = 'build' if (on_master_branch or detached_head) else sane_branch_name(branch_name)
        new_version = current_version.bump_patch().replace(build=f"{build_token}.{distance}")
        return f"{new_version}"


def find_latest_tag_in_path(repo: Repo, logger: Logger):
    valid_tags = [t for t in repo.tags if semver.VersionInfo.isvalid(t.name)]
    logger.debug("Valid tags are: %s", [t.name for t in valid_tags])
    if len(valid_tags) > 0:
        valid_tags.reverse()
        try:
            commits = list(repo.iter_commits(repo.active_branch))
            branch_name = repo.active_branch.name
        except TypeError:
            logger.debug("Have detached head")
            commits = list(repo.iter_commits())
            branch_name = None
        for valid_tag in valid_tags:
            logger.debug("Checking if %s in %s", valid_tag.commit, commits)
            if valid_tag.commit in commits:
                latest_tag = valid_tag
                distance = commits.index(latest_tag.commit)
                return latest_tag, distance, branch_name
    # didnt find anything...
    logger.info("No valid tags found")
    raise NoValidTagFoundError("No valid version tag found")


def sane_branch_name(branch_name):
    if '/' in branch_name:
        branch_part = branch_name.split('/')[-1]
    else:
        branch_part = branch_name
    return re.sub('[^a-z0-9]', '', branch_part.lower())
