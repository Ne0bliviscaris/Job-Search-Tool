import logging


def updater_log(name="Updater"):
    """Return logger with fixed-width column formatting."""
    FORMAT = "%(asctime)-20s  -  %(levelname)-7s -  %(name)-6s -  %(message)s"

    logging.basicConfig(
        filename="modules\\updater\\updater.log",
        level=logging.INFO,
        format=FORMAT,
        datefmt="%Y-%m-%d  %H:%M:%S",
    )

    return logging.getLogger(name)
