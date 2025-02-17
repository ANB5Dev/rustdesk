#!/usr/bin/env python3

import os
import sys
import json
from glob import glob
import shutil

def main():

    if len(sys.argv) < 2:
        print(r"Usage: python move_images.py '<JSON>', eg:")
        print('python move_images.py \'{ \\"app_name\\": \\"ASCI Hulp op Afstand\\", \\"email\\": \\"info@asci.nl\\", \\"description\\": \\"ASCI Hulp op Afstand Remote Desktop Application\\", \\"company\\": \\"ASCI Technologies BV\\", \\"website\\": \\"https://asci.nl\\", \\"privacy_url\\": \\"https://asci.nl\\", \\"identifier\\": \\"nl.asci.hulpopafstand\\", \\"copyright\\": \\"ASCI Technologies BV\\", \\"images\\": \\"asci\\", \\"incoming_only\\": true, \\"debug\\": true }\'')
        sys.exit(1)

    config_arg = sys.argv[1]
    config_dict = json.loads(config_arg)
    print('config:', config_dict)
    dir = f'customization/images/{config_dict["images"]}/generated'

    print(f'\nMoving images from: {dir}\n')
    images = glob(f'{dir}/**/*.png', recursive=True) + glob(f'{dir}/**/*.svg', recursive=True) + glob(f'{dir}/**/*.ico', recursive=True)
    for i in images:
        print(f'{i} -> {os.path.relpath(i, dir)}')
        shutil.copy(i, os.path.relpath(i, dir))
        

if __name__ == '__main__':
    main()