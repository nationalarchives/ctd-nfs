import uuid
from pathlib import Path
import json

import pprint

pretty_printer = pprint.PrettyPrinter(indent=4)


filenames = ["MAF32-168-1_1.tif", "MAF32-168-1_2.tif", 
             "MAF32-168-1_115.tif", "MAF32-168-1_116.tif",
             "MAF32-168-1_215.tif", "MAF32-168-1_216.tif",
             "MAF32-168-1_342.tif", "MAF32-168-1_343.tif",
]


IAID = str(uuid.uuid4())
        

filenames = ["MAF32-168-1_1.tif", "MAF32-168-1_2.tif", 
             "MAF32-168-1_115.tif", "MAF32-168-1_116.tif",
             "MAF32-168-1_215.tif", "MAF32-168-1_216.tif",
             "MAF32-168-1_342.tif", "MAF32-168-1_343.tif",
]


IAID = str(uuid.uuid4())

images = [{'file_name': filename, 'file_id': str(uuid.uuid4()), 'sequence_no': idx} for idx, filename in enumerate(filenames, start=1)]
keys = {
    'reference': "MAF 32/168/1",
    'IAID': IAID,
    'images': images,
}

pretty_printer.pprint(keys)
filename = Path("image_map.json")
with open(filename, 'w') as f:
    json.dump(keys, f, indent=4)