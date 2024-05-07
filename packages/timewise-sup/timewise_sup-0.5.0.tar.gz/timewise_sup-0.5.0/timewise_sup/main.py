import logging
import json
from argparse import ArgumentParser
import re
from datetime import datetime
from subprocess import check_output
from pathlib import Path

from timewise_sup.config_loader import TimewiseSUPConfigLoader


logger = logging.getLogger(__name__)


def main():
    parser = ArgumentParser()
    parser.add_argument("config", type=str, help="Path to timewise_sup config file")
    parser.add_argument("-l", "--logging-level", default="INFO", type=str)
    cfg = vars(parser.parse_args())

    logging_level = cfg.pop("logging_level")
    logging.getLogger("timewise_sup").setLevel(logging_level)
    logging.getLogger("timewise").setLevel(logging_level)
    logger.debug(f"Running timewise_sup with args {json.dumps(cfg, indent=4)}")
    TimewiseSUPConfigLoader.run_yaml(cfg["config"])


def bump_version():
    """
    Bump the version number in timewise_sup/__init__.py file, codemeta.json file, pyproject.toml and docs/source/conf.py
    """

    parser = ArgumentParser()
    parser.add_argument(
        "--which",
        type=str,
        help="Which version number to bump",
        choices=['patch', 'minor', 'major'],
        default="patch"
    )
    parser.add_argument("--dry-run", action="store_true", help="Actually bump the version number")
    parser.add_argument("--publish", action="store_true", help="Push to git and publish to pypi")
    parser.add_argument("--fixed-version", type=str, help="Use a fixed version number instead of bumping")
    parser.add_argument("-l", "--logging-level", default="INFO", type=str)
    cfg = parser.parse_args()

    logging.getLogger("timewise_sup").setLevel(cfg.logging_level)

    base_directory = Path(__file__).parent.parent
    files = {
        "init": "timewise_sup/__init__.py",
        "meta": "codemeta.json",
        "setup": "pyproject.toml",
        "doc_conf": "docs/source/conf.py"
    }
    paths = {k: base_directory / v for k, v in files.items()}

    if cfg.which not in ["patch", "minor", "major"]:
        raise ValueError(f"which must be either of 'patch', 'minor' or 'major' but {cfg.which} was given!")

    # timewise/__init__.py
    with open(paths["init"], "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("__version__"):
            version_line = line
            break

    version = re.findall(r"\d+\.\d+\.\d+", version_line)[0]
    major, minor, patch = [int(v) for v in version.split(".")]
    logger.debug(f"Current version: {version}")

    if cfg.which == "patch":
        patch += 1
    elif cfg.which == "minor":
        minor += 1
        patch = 0
    elif cfg.which == "major":
        major += 1
        minor = 0
        patch = 0

    new_version = cfg.fixed_version or f"{major}.{minor}.{patch}"
    logger.info(f"Bumping version from {version} to {new_version}")
    new_version_line = f'__version__ = "{new_version}"\n'
    lines[i] = new_version_line

    # codemeta.json
    with open(paths["meta"], "r") as f:
        codemeta = json.load(f)

    codemeta["version"] = new_version
    codemeta["softwareVersion"] = new_version
    codemeta["dateModified"] = datetime.now().strftime("%Y-%m-%d")
    codemeta["name"] = codemeta["name"].strip("v" + version) + "v" + new_version
    if cfg.publish:
        codemeta["datePublished"] = datetime.now().strftime("%Y-%m-%d")

    # pyproject.toml
    with open(paths["setup"], "r") as f:
        pyproject = f.readlines()

    for i, line in enumerate(pyproject):
        if line.startswith("version"):
            break

    pyproject[i] = f'version = "{new_version}"\n'

    # docs/source/conf.py
    with open(paths["doc_conf"], "r") as f:
        conf = f.readlines()

    for i, line in enumerate(conf):
        if line.startswith("release"):
            break

    conf[i] = f"release = 'v{new_version}'\n"

    # log
    for fn, content in zip(list(files.values()),
                           ["".join(lines), json.dumps(codemeta, indent=4), "".join(pyproject), "".join(conf)]):
        logger.debug(f"New content of {fn}:")
        logger.debug("\n" + content)

    # write files
    if not cfg.dry_run:
        logger.info("writing new version to timewise_sup/__init__.py")
        with open(paths["init"], "w") as f:
            f.writelines(lines)

        logger.info("writing new version to codemeta.json")
        with open(paths["meta"], "w") as f:
            json.dump(codemeta, f, indent=4)

        logger.info("writing new version to pyproject.toml")
        with open(paths["setup"], "w") as f:
            f.writelines(pyproject)

        logger.info("writing new version to docs/source/conf.py")
        with open(paths["doc_conf"], "w") as f:
            f.writelines(conf)

        if cfg.publish:
            current_branch = [i.split("* ")[-1] for i in check_output(["git", "branch"]).decode().split("\n") if "*" in i][0]
            if current_branch != "main":
                raise ValueError(f"Current branch is {current_branch} but must be main if you want to publish the version!")

            logger.info("Committing changes to git")
            check_output(["git", "add"] + list(paths.values()))
            check_output(["git", "commit", "-m", f"Bump version from {version} to {new_version}"])
            check_output(["git", "push"])

            logger.info("Tagging commit")
            check_output(["git", "tag", "-a", f"v{new_version}", "-m", f"v{new_version}"])

            logger.info(
                "wait until build succeeds on https://gitlab.desy.de/jannisnecker/timewise_sup/-/pipelines"
                " and then push tag to git with 'git push --tags'"
            )
