#!/usr/bin/env python

from pathlib import Path
import shutil
from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from typing import BinaryIO

from chris_plugin import chris_plugin

from tqdm import tqdm
import requests
import tarfile
import shutil
import hashlib

from requests.exceptions import RequestException

__version__ = "2.0.2"

DISPLAY_TITLE = r"""

       _                  _                     _       _            _
      | |                | |                   | |     | |          | |
 _ __ | |______ ___ _ __ | | ___  ___ _ __   __| | __ _| |_ __ _  __| |___
| '_ \| |______/ __| '_ \| |/ _ \/ _ \ '_ \ / _` |/ _` | __/ _` |/ _` / __|
| |_) | |      \__ \ |_) | |  __/  __/ | | | (_| | (_| | || (_| | (_| \__ \
| .__/|_|      |___/ .__/|_|\___|\___|_| |_|\__,_|\__,_|\__\__,_|\__,_|___/
| |                | |
|_|                |_|

"""


parser = ArgumentParser(
    description="""
    A ChRIS DS plugin that downloads a spleen data set for training
    and inference. Based off a MONAI exemplar:
                                    """,
    formatter_class=ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "--url",
    default="https://msd-for-monai.s3-us-west-2.amazonaws.com/Task09_Spleen.tar",
    help="url of remote tar archive file",
)
parser.add_argument(
    "--md5",
    default="410d4a301da4e5b2f6f86ec3ddba524e",
    help="md5 sum of remote resource once downloaded",
)
parser.add_argument(
    "--skipDownload",
    default=False,
    action="store_true",
    help="""If specified, skip the download. Only useful for debugging/testing really.""",
)
parser.add_argument(
    "--trainingOnly",
    default=False,
    action="store_true",
    help="""If specified, only preserve the training data (saving about 462Mb)""",
)
parser.add_argument(
    "--testingOnly",
    default=False,
    action="store_true",
    help="""If specified, only preserve the testing data (saving about 1.2Gb)""",
)
parser.add_argument(
    "--copyInputDir",
    default=False,
    action="store_true",
    help="""If specified, copy the inputDir to outputDir""",
)
parser.add_argument(
    "--man",
    default=False,
    action="store_true",
    help="""If specified, show simple manual page""",
)
parser.add_argument(
    "-V", "--version", action="version", version=f"%(prog)s {__version__}"
)


def man():
    man: str = """

    NAME
        spleendatads

    SYNOPSIS
        spleendatads    [--url <url>]                   \\
                        [--md5 <sum>]                   \\
                        [--skipDownload]                \\
                        [--trainingOnly]                \\
                        [--testingOnly]                 \\
                        [--man]                         \\
                        [--copyInputDir]                \\
                        <inputDir> <outputDir>

    DESCRIPTION

        `spleendatads` pulls a specific resource from the internet (a tar/gz) file
        and extracts its contents, optionally also checking the md5sum.

    ARGS:
        [--url <url>]
        The url of the resource (file) to download.

        [--md5 <sum>]
        The md5 sum of this file. Set to empty string to ignore.

        [--skipDownload]
        If specified, skip the download. Mostly for debugging.

        [--trainingOnly]
        If specified, keep only the training images.

        [--testingOnly]
        If specified, keep only the testing images.

        [--man]
        If specified, show this manual page.

        [--copyInputDir]
        If specified, copy the input directory to the output.

    """
    return man


def file_downloadAndExtract(url: str, toFile: Path) -> bool:
    status: bool = True

    try:
        resp: requests.Response = requests.get(url, stream=True)
        resp.raise_for_status()
        totalSize: int = int(resp.headers.get("Content-Length", 0))
        print(f"Download size {totalSize}")
        f: BinaryIO
        chunk: bytes
        blockSize: int = 8192

        with tqdm(total=totalSize, unit="iB", unit_scale=True) as progress_bar:
            with open(toFile, "wb") as f:
                for chunk in resp.iter_content(chunk_size=blockSize):
                    if chunk:
                        progress_bar.update(len(chunk))
                        f.write(chunk)

        tar: tarfile.TarFile
        with tarfile.open(toFile, "r") as tar:
            totalMembers = sum(member.size for member in tar.getmembers())
            progress_bar = tqdm(
                total=totalMembers, unit="iB", unit_scale=True, desc="Extracting"
            )
            for member in tar:
                tar.extract(member, toFile.parent)
                progress_bar.update(member.size)
            progress_bar.close()
    except RequestException as e:
        print(f"Error downloading the file {e}")
    except tarfile.TarError as e:
        print(f"Error extracting the archive {e}")
    except Exception as e:
        print(f"An unexpected error occurred {e}")

    return status


def dir_findAndDelete(startdir: Path, target: str):
    for item in startdir.iterdir():
        if item.is_dir():
            if item.name == target:
                shutil.rmtree(str(item))
                # item.rmdir()
                print(f"Deleted directory: {target}")
                break
            else:
                dir_findAndDelete(item, target)


# The main function of this *ChRIS* plugin is denoted by this ``@chris_plugin`` "decorator."
# Some metadata about the plugin is specified here. There is more metadata specified in setup.py.
#
# documentation: https://fnndsc.github.io/chris_plugin/chris_plugin.html#chris_plugin
@chris_plugin(
    parser=parser,
    title="Spleen data downloader",
    category="",  # ref. https://chrisstore.co/plugins
    min_memory_limit="100Mi",  # supported units: Mi, Gi
    min_cpu_limit="1000m",  # millicores, e.g. "1000m" = 1 CPU core
    min_gpu_limit=0,  # set min_gpu_limit=1 to enable GPU
)
def main(options: Namespace, inputdir: Path, outputdir: Path):
    """
    *ChRIS* plugins usually have two positional arguments: an **input directory** containing
    input files and an **output directory** where to write output files. Command-line arguments
    are passed to this main method implicitly when ``main()`` is called below without parameters.

    :param options: non-positional arguments parsed by the parser given to @chris_plugin
    :param inputdir: directory containing (read-only) input files
    :param outputdir: directory where to write output files
    """

    print(DISPLAY_TITLE)
    resource: str = options.url
    md5: str = options.md5

    if options.man:
        print(man())
        return

    compressed_file: Path = outputdir / "Task09_Spleen.tar"
    data_dir: Path = outputdir / "Task09_Spleen"
    if not data_dir.exists() or options.skipDownload:
        file_downloadAndExtract(resource, compressed_file)
        # download_and_extract(resource, str(compressed_file), str(outputdir), md5)

    if options.copyInputDir:
        shutil.copytree(str(inputdir), str(outputdir))

    if compressed_file.exists():
        compressed_file.unlink()
    if options.trainingOnly:
        dir_findAndDelete(outputdir, "imagesTs")
    if options.testingOnly:
        dir_findAndDelete(outputdir, "imagesTr")
        dir_findAndDelete(outputdir, "labelsTr")


if __name__ == "__main__":
    main()
