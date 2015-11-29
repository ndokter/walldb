from io import BytesIO

from PIL import Image


class UnsupportedFileExtensionError(Exception):
    pass


def create_thumbnail(image_file, file_extension, thumbnail_width=300, thumbnail_height=200):
    if file_extension not in ('jpeg', 'png'):
        raise UnsupportedFileExtensionError(
            'File extension: \'{extension}\' not supported for thumbnail',
            file_extension
        )

    img = Image.open(image_file)

    src_width, src_height = img.size
    src_ratio = float(src_width) / float(src_height)
    dst_width, dst_height = thumbnail_width, thumbnail_height
    dst_ratio = float(dst_width) / float(dst_height)

    if dst_ratio < src_ratio:
        crop_height = src_height
        crop_width = crop_height * dst_ratio
        x_offset = int(float(src_width - crop_width) / 2)
        y_offset = 0
    else:
        crop_width = src_width
        crop_height = crop_width / dst_ratio
        x_offset = 0
        y_offset = int(float(src_height - crop_height) / 3)

    img = img.crop((x_offset,
                    y_offset,
                    x_offset+int(crop_width),
                    y_offset+int(crop_height)))

    img = img.resize((int(dst_width), int(dst_height)), Image.ANTIALIAS)

    temp_handle = BytesIO()

    img.save(temp_handle, file_extension, quality=90)

    temp_handle.seek(0)

    return temp_handle.read()
