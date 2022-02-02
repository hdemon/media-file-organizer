import os
import sys
import imagehash
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import PIL

root_path = sys.argv[1]
dest_root_path = sys.argv[2]

image_files = []
files = [os.path.join(root_path, path) for path in os.listdir(root_path)]
for file in files:
    try:
        # TODO: put a condition to make a dedicated logic for images and movies
        image = None
        image = Image.open(file)
        # Set hash_size 128 (default: 8) to find out even minor differences.
        # https://pillow.readthedocs.io/en/stable/reference/Image.html#functions
        hash = imagehash.phash(image, hash_size=16)
        print(file)
        new_file_name = ('%s' % hash) + '.' + os.path.basename(file)
        date_object = {}

        exif = image._getexif()
        # If the file has exif the "DateTimeOriginal" on it will be used for a dest directory name
        # instead of ctime.
        if exif != None:
            exif_table = {}
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                exif_table[tag] = value
            # see here to know about Date Time Original on exif
            # https://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif/datetimeoriginal.html
            date_time_original = exif_table['DateTimeOriginal']
            date_object = datetime.strptime(date_time_original, '%Y:%m:%d %H:%M:%S')
        else:
            unixtime_float = os.path.getctime(file)
            date_object = datetime.fromtimestamp(unixtime_float)

        new_dest_directory = dest_root_path + '/' + datetime.strftime(date_object, '%Y-%m-%d')
        new_dest_file = new_dest_directory + '/' + new_file_name
        print(new_dest_file)

        if not os.path.isdir(new_dest_directory):
            print("make directory")
            os.mkdir(new_dest_directory)

        print("copy file")
        shutil.copy2(file, new_dest_file)
        os.remove(file)
    except FileNotFoundError: # If the file cannot be found.
        print('%s' % file, ' was not found.')
        continue
    except PIL.UnidentifiedImageError: # If the image cannot be opened and identified.
        print('%s' % file, ' could not be opened and identified.')
        continue
    except ValueError: # If the mode is not “r”, or if a StringIO instance is used for fp.
        print('%s' % file, ' could not be opened maybe because of it doesn\'t have \'r\' mode.')
        continue
    except NameError:
        print("name error")
        continue
    except:
        print(sys.exc_info()[0])
        continue
