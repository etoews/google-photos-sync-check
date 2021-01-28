import argparse
import logging
import os


logger = logging.getLogger(__name__)


def cleanup(path):
    for dirpath, dirnames, files in sorted(os.walk(path)):
        logger.info(f"Dir: {dirpath}")
        for filename in sorted(files):
            logger.info(f"File:   {filename}")

            if filename.endswith('-edited.HEIC'):
                normal_filename = filename.replace('-edited.HEIC', '.HEIC')
                normal_filename_path = os.path.join(dirpath, normal_filename)

                if os.path.exists(normal_filename_path):
                    logger.info(f"Delete: {normal_filename}")
                    os.remove(normal_filename_path)

            if filename.endswith('HEIC'):
                mov_filename = filename.replace('HEIC', 'MOV')
                mov_filename_path = os.path.join(dirpath, mov_filename)

                if os.path.exists(mov_filename_path):
                    logger.info(f"Delete: {mov_filename}")
                    os.remove(mov_filename_path)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Local file path to takeout photo albums to cleanup')

    return parser.parse_args()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s.%(msecs)03d, %(levelname)s, %(message)s', datefmt='%Y-%m-%dT%H:%M:%S', level=logging.DEBUG)

    args = get_args()

    cleanup(args.path)
