#!/usr/bin/env python3

import argparse
import logging
import os
import subprocess


def get_depth(rootpath, path):
    """
    Get the depth of a given path. Only works if the given path is an
    abspath (os.path.abspath).

    :param rootpath: the root of the directory tree (relative to this the depth
        will be calculated)
    :type rootpath: str
    :param path: the path whose depth should be evaluated
    :type path: str
    :return: the depth of the given path
    :rtype: int
    """
    return path[len(rootpath):].count(os.path.sep)


def get_sync(path, depth):
    """
    Return a list of all directories and files to be synced. It will recurse up
    to a depth given by the parameter `depth`.

    :param path: the root of the directory tree
    :type path: str
    :param depth: the recurse depth
    :type depth: int
    :return: list of directories to be synced
    :rtype: list
    """
    dirlist = list()
    filelist = list()
    path = os.path.abspath(path)

    for root, dirs, files in os.walk(path, topdown=True):
        current_depth = get_depth(path, root)
        if current_depth < depth - 1:
            for file in files:
                abspath = os.path.join(root, file)
                filelist.append(abspath[len(path)+len(os.path.sep):])
        if current_depth == depth - 1:
            if len(dirs) != 0:
                for dir in dirs:
                    abspath = os.path.join(root, dir)
                    dirlist.append(abspath[len(path)+len(os.path.sep):])
            if len(files) != 0:
                for file in files:
                    abspath = os.path.join(root, file)
                    filelist.append(abspath[len(path)+len(os.path.sep):])

    return dirlist, filelist


def perform_sync(source, destination, dirlist, filelist, options,
                 max_retries=10, *args, **kwargs):
    """
    Perform the syncronization with rsync.

    :param source: the source directory
    :type source: str
    :param destination: the destination to sync to
    :type destination: str
    :param dirlist: The list of all directories to be synched. Needs to be a
        list of paths relative to src.
    :type dirlist: list
    :param filelist: The list of all files to be synched. Needs to be a list of
        paths relative to src.
    :param options: The options to pass to rsync.
    :type options: str
    :param max_retries: the maximum amount of retries before the job fails
    :type max_retries: int
    :return: exit code
    :rtype: int
    """
    try:
        dry_run = kwargs['dry_run']
    except KeyError:
        dry_run = False

    sync_objects = dirlist + filelist

    if len(destination.split(":")) == 2:
        remote, remote_dir = destination.split(":")
        remote += ":"       # add the : delimiter to the remote variable
    else:
        remote = ""
        remote_dir = destination

    for sync_object in sync_objects:
        src = os.path.join(source, sync_object)
        dst = os.path.join(remote_dir, sync_object)

        logging.info(f"Syncing {src}")

        if not dry_run:
            retry = 0
            proc = subprocess.run(
                ["rsync", f"-{options}", src, f"{remote}{dst}"])

            while proc.returncode != 0:
                logging.info(f"Failed sync of {src}. Retrying (retry={retry})")
                retry += 1
                proc = subprocess.run(
                    ["rsync", f"-{options}", src, f"{remote}{dst}"])
                if retry >= max_retries:
                    logging.critical(f"Reached maximum amount of retries "
                                     f"(max_retries={max_retries}). Sync job "
                                     f"{sync_object} failed. Aborting.")
                    return 1

        else:
            print(f"rsync -{options} {src} {remote}{dst}")

    return 0


def main():
    """
    The main function to be run for the script in cli mode.
    :return: Exitcode
    :rtype: int
    """
    description = """
        Lagsync is an rsync based utility for syncing files over flakey connections.
        It accomplishes this by splitting the sync process into smaller chunks.
        These chunks are calculated by providing a depth. The directories at the
        given depth in the directory tree are then separately synced to the
        destination.
        """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("source", metavar="src",
                        help="The source (rootpath) of the files to be synced")
    parser.add_argument("destination", metavar="dst",
                        help="The destination for the sync.")
    parser.add_argument("-o", "--rsync-options", metavar="rsync_opt",
                        default="rtlz",
                        help="Options for the rsync job. Default is 'rtlz'")
    parser.add_argument("-d", "--depth", type=int, default=2,
                        help="The depth of the directory tree which will be"
                             "used for chunking of the rsync jobs.")
    parser.add_argument("-r", "--max-retries", type=int, default=10,
                        help="The maximum amount of retries for the rsync job"
                             "per chunk")
    parser.add_argument("--dry-run", action="store_true",
                        help="Perform a dry run, which will only print out"
                             "the resync jobs instead of running them.")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="verbose mode")

    args = parser.parse_args()

    # enable verbose logging
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    # perform sync
    dirlist, filelist = get_sync(args.source, args.depth)
    return perform_sync(args.source, args.destination, dirlist, filelist,
                        args.rsync_options, max_retries=args.max_retries,
                        dry_run=args.dry_run)


if __name__ == '__main__':
    main()
