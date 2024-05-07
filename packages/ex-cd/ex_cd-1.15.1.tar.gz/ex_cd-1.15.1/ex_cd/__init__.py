from .config import build_parser, read_config
from .history import get_latest_url, put_history_placeholder
from .output import initialize_logging
from .download import download_gallery_history


def main():
    parser = build_parser()
    args = parser.parse_args()
    logger = initialize_logging(args.loglevel)
    config = read_config(args, logger)
    logger.info(f"Parsed confg: {args}")
    for url in args.urls:
        url, gallery_dir = get_latest_url(url, config, logger)
        logger.info(f"Downloading: {url} -> {gallery_dir}")
        put_history_placeholder(url, gallery_dir, config, logger)
        for _ in range(config['retry']):
            try:
                download_gallery_history(url, gallery_dir, config, logger)
            except Exception as e:
                logger.error("download_gallery_history failed, retry:", e)
                continue
            return
