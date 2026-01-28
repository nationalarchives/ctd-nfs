from collections import OrderedDict
import pprint
from uuid import UUID

from src.farm_builder import Form, Image, initialise_forms_mapping

# forms = [
#     OrderedDict({'C 47/SSY': [], 'C 49/SSY': [], 'C51/SSY': [], 'SF': [], 'SF C69/SSY': [], 'B496/EI': [Form(images=[Image(filename='MAF32-194-1_59.tif', id=UUID('7c8c80ef-b8bd-4213-ae8a-1c78895acb0a')), Image(filename='MAF32-194-1_60.tif', id=UUID('8921a2ac-f4c2-4784-ac90-a0f705f19b99'))], field_info_date='06-Feb-42', primary_record_date='12-Feb-43')], 'Other': [], 'Cover': []}),
#     OrderedDict({'C 47/SSY': [Form(images=[Image(filename='MAF32-194-1_75.tif', id=UUID('c8b2129a-59cc-4448-8d9f-3fb9cb41c4e6')), Image(filename='MAF32-194-1_76.tif', id=UUID('293e9643-380a-4d15-86d8-111fdebd8494'))], field_info_date='', primary_record_date='')], 'C 49/SSY': [], 'C51/SSY': [], 'SF': [], 'SF C69/SSY': [], 'B496/EI': [], 'Other': [], 'Cover': []}),
#     OrderedDict({'C 47/SSY': [], 'C 49/SSY': [], 'C51/SSY': [], 'SF': [], 'SF C69/SSY': [], 'B496/EI': [Form(images=[Image(filename='MAF32-228-1_23.tif', id=UUID('9fe31aaf-5533-4794-ad54-53a70d637864')), Image(filename='MAF32-228-1_24.tif', id=UUID('684bffc5-d9f1-45ef-acc0-7555957c5c7c'))], field_info_date='*', primary_record_date='19 April 1943')], 'Other': [], 'Cover': []}),
#     OrderedDict({'C 47/SSY': [], 'C 49/SSY': [], 'C51/SSY': [], 'SF': [], 'SF C69/SSY': [], 'B496/EI': [Form(images=[Image(filename='MAF32-247-23_75.tif', id=UUID('fd5288e7-b291-4593-8a50-2833eb7d221f')), Image(filename='MAF32-247-23_76.tif', id=UUID('81436e6e-5b96-4616-87f1-63490031688e'))], field_info_date='30 January 1942', primary_record_date='*')], 'Other': [], 'Cover': []})
# ]

# pretty = pprint.PrettyPrinter(indent=4)

# for form_set in forms:
#     pretty.pprint(form_set)

forms = initialise_forms_mapping()
form_data = [
    ["MAF32-167-29_1.tif","MAF32-167-29_2.tif", "C51/SSY", "", "",],
    ["MAF32-167-29_23.tif", "MAF32-167-29_24.tif", "B496/EI", "November 1942", "December 1943",],
    ["MAF32-167-29_25.tif", "", "B496/EI", "*", "*",],
    ["MAF32-167-29_56.tif", "MAF32-167-29_57.tif", "C 47/SSY", "", "",],
    ["MAF32-167-29_82.tif", "MAF32-167-29_83.tif", "SF", "", "",],
]
fields = ["filename_1", "filename_2", "document_type", "field_info_date", "primary_record_date",]

for data in form_data:
    item = dict(zip(fields, data))
    pics = [Image(f)
        for f in ["filename_1", "filename_2"]
    ]
    forms[item['document_type']] = Form(images=pics, field_info_date=item['field_info_date'], primary_record_date=item['primary_record_date'])
