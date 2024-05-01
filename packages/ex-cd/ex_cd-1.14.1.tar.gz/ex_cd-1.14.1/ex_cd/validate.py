import os
import json
import hashlib
from .common import META_FOLDER
from .meta import _valid_gallery_meta, _get_image_tokens


VALIDATE_COMPLETED_FILE = 'ValidateCompleted'
DOWNLOAD_RESUME_FILE = 'DownloadResume'


def _validate_gallery(url, gallery_dir, config, logger):
    """validate the gallery"""
    ok_file = os.path.join(gallery_dir, META_FOLDER, VALIDATE_COMPLETED_FILE)
    if os.path.isfile(ok_file):  # if valid
        return True  # exit

    # check if has enough metadata json files
    if not _valid_gallery_meta(url, gallery_dir, config, logger):
        return False
    site, gid, image_tokens, metafiles = _get_image_tokens(url, gallery_dir, config, logger)

    # check if has enough image files
    images = []
    for img in os.listdir(gallery_dir):
        if img == META_FOLDER:
            continue
        images.append(img)

    resume_url = url
    ok = True
    # check if image content SHA1 match image_token
    for i, (image_token, metafile) in enumerate(zip(image_tokens, metafiles)):
        img = metafile[0:-5]
        if img not in images:
            logger.error(f"Invalid {gallery_dir}: no image {img} for {metafile}")
            resume_url = f"{site}/s/{image_token}/{gid}-{i+1}"
            ok = False
            break
        # compare image_token
        imgfile = os.path.join(gallery_dir, img)
        try:
            with open(imgfile, mode="rb") as fp:
                sha1 = hashlib.sha1(fp.read()).hexdigest()
            if image_token != sha1[0:10]:
                logger.error(f"Invalid {imgfile}: image token not match, {image_token} != {sha1}, delete the image")
                os.remove(imgfile)
                resume_url = f"{site}/s/{image_token}/{gid}-{i+1}"
                ok = False
                break
        except Exception as e:
            logger.error(f"Invalid {imgfile}: cannot compare token, {e}, delete the image")
            os.remove(imgfile)
            resume_url = f"{site}/s/{image_token}/{gid}-{i+1}"
            ok = False
            break
    if ok:
        with open(ok_file, "w", encoding='utf8'):
            return True  # record that this gallery has been validated
    else:
        resume_file = os.path.join(gallery_dir, META_FOLDER, DOWNLOAD_RESUME_FILE)
        with open(resume_file, "w", encoding='utf8') as fp:
            fp.write(resume_url)
            logger.error(f"Invalid {gallery_dir}: no enough metadata files, should resume from {resume_url}")
        return False
