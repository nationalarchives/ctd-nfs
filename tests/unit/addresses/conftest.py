import pytest


@pytest.fixture()
def addresses():
	return [
		{
			'final': "The Old Hall, Ashwell, Oakham, Rutland",
			'original': [
				"The Old Hall, Ashwell, Oakham, Rutland","Old Hall, Ashwell, Oakham, Rutland",
				"Old Hall, Ashwell, Oakham, Rutland",
			],
		},
		{
			'final': "Honington, Grantham, Ashwell, Oakham, Rutland",
			'original': [
				"Honington, Grantham, Ashwell, Oakham, Rutland","Honington, Grantham",
				"Honington, Grantham",
			],
		},
		{
			'final': "South View, Ashwell, Oakham, Rutland",
			'original': [
				"South View, Ashwell, Oakham, Rutland","Ashwell, Oakham, Rutland",
				"Ashwell, Oakham, Rutland",
			],
		},
		{
			'final': "Woodside, Ashwell, Near Oakham, Rutland",
			'original': [
				"Woodside, Ashwell, Near Oakham, Rutland","Woodside, Ashwell, Oakham, Rutland",
				"Woodside, Ashwell, Oakham, Rutland",
			],
		},
		{
			'final': "Maycroft Farm, Ashwell, Oakham, Rutland",
			'original': [
				"Maycroft Farm, Ashwell, Oakham, Rutland","Ashwell, Oakham, Rutland",
				"Maycroft Farm, Ashwell, Oakham, Rutland",
			],
		},
		{
			'final': "Baines Farm, Ashwell, Oakham, Rutland",
			'original': [
				"Ashwell, Oakham, Rutland","Baines Farm, Ashwell, Oakham, Rutland",
				"Baines Farm, Ashwell, Oakham, Rutland",
			],
		},
		{
			'final': "Butcher, Vergette Street, Peterborough, Northamptonshire",
			'original': [
				"Vergette Street, Peterborough","Vergette Street, Peterborough, Northamptonshire",
				"Butcher, Vergette Street, Peterborough, Northamptonshire",
				"Butcher, Vergette Street, Peterborough, Northamptonshire",
			],
		},
		# {
		# 	'final': "The Hall, Ashwell, Oakham, Rutland",
		# 	'original': [
		# 		"Ashwell Hall, Oakham",
		# 		"The Hall, Ashwell, Oakham, Rutland",
		# 		"The Hall, Ashwell, Oakham, Rutland",
		# 		"The Hall, Ashwell, Oakham, Rutland",
		# 	],
		# },
		# {
		# 	'final': "Rotherby, Melton Mowbray/Home Farm, Rotherby, Leicester",
		# 	'original': [
		# 		"Rotherby, Melton Mowbray",
		# 		"Home Farm, Rotherby, Leicester",
		# 		"Home Farm, Rotherby, Leicester",
		# 	],
		# },
		# {
		# 	'final': "Ashwell Lodge, Near Oakham, Rutland/Poultry Farm, Ashwell, Oakham, Rutland",
		# 	'original': [
		# 		"Ashwell Lodge, Near Oakham, Rutland",
		# 		"Poultry Farm, Ashwell, Oakham, Rutland",
		# 		"Poultry Farm, Ashwell, Oakham, Rutland",
		# 	],
		# },
		# {
		# 	'final': "c/o Capt Hornsby, Westfield Cottage, Ashwell, Oakham, Rutland",
		# 	'original': [
		# 		"Westfield Cottage, Ashwell, Grange, Oakham",
		# 		"c/o Capt Hornsby, Westfield Cottage, Ashwell, Oakham, Rutland",
		# 		"c/o Capt Hornsby, Westfield Cottage, Ashwell, Oakham, Rutland",
		# 	],
		# },
		# {
		# 	'final': "Burrough Manor, Melton Mowbray, Cottesmore Hunt Kennels, Oakham/The Kennels, Cottesmore, Rutland/Borough Manor, Melton Mowbray, Oakham",
		# 	'original': [
		# 		"Burrough Manor, Melton Mowbray, Cottesmore Hunt Kennels, Oakham",
		# 		"The Kennels, Cottesmore, Rutland",
		# 		"Borough Manor, Melton Mowbray, Oakham",
		# 	],
		# },
		# {
		# 	'final': "The Old Rectory, Caldecott, Market Harborough",
		# 	'original': [
		# 		"The Old Rectory, Caldecott, Market Harborough",
		# 		"The Old Rectory, Caldecott, Market Harborough, Leicestershire",
		# 		"The Old Rectory, Caldecott, Market Harborough, Rutland",
		# 		"The Old Rectory, Caldecott, Market Harborough, Rutland",
		# 	],
		# },
		# {
		# 	'final': "Green Cottage, Langham, Oakham, Rutland",
		# 	'original': [
		# 		"Green Cottage, Langham, Oakham",
		# 		"Langham, Oakham, Rutland",
		# 		"Langham, Oakham, Rutland",
		# 	],
		# },
		# {
		# 	'final': "Edithweston/Edith Weston, Oakham, Rutland",
		# 	'original': [
		# 		"The Yews, Edith Weston, Oakham",
		# 		"Edithweston, Oakham, Rutland",
		# 		"Edithweston, Oakham, Rutland",
		# 	],
		# },
		# {
		# 	'final': "47 Edithweston/Edith Weston, Near Oakham, Rutland",
		# 	'original': [
		# 		"47 Edith Weston, Near Oakham, Rutland",
		# 		"Edithweston, Oakham, Rutland",
		# 		"47 Edithweston, Near Oakham, Rutland",
		# 		"Edithweston, Oakham, Rutland",
		# 	],
		# }
	]	


# @pytest.fixture()
# def address():
# 	return({
# 		"1": ["Butlers Court Farm, Boddington, Gloucestershire", "Butlers Court, Boddington, Near Cheltenham", "Butlers Court, Boddington", "Butlers Court Farm, Boddington, Gloucestershire"], 
# 		"2": ["Whitehall, Hayden Hill, Cheltenham, Gloucestershire", "Whitehall Farm, Hayden, Cheltenham", "Whitehall Farm, Hayden, Cheltenham", "Whitehall, Hayden Hill, Cheltenham, Gloucestershire"], 
# 		"3": ["Boddington House Farm, Boddington, Gloucestershire", "Boddington House Farm, Boddington, Cheltenham", "Boddington House Farm, Near Cheltenham", "Boddington House, Boddington, Gloucestershire"],
# 		"6": ["Slate Mill, Boddington, Near Cheltenham, Gloucestershire","Slade Mill, Boddington, Cheltenham", "Slate Mill, Boddington", "Slate Mill, Boddington, Near Cheltenham, Gloucestershire"],
# 		"7": ["Barrow Court, Boddington, Cheltenham, Gloucestershire", "14, Foregate Street, Worcester", "Barrow Court, Boddington", "Barrow Court, Boddington, Cheltenham, Gloucestershire"],
# 		"9": ["Manor Farm, Boddington, Near Cheltenham, Gloucestershire", "Guiting House, Temple Guiting, Gloucestershire", "Manor Farm, Boddington", "Manor Farm, Boddington, Near Cheltenham, Gloucestershire"],
# 		"10": ["c/o Mr S Fluck, Pilgrove Farm, Hayden Hill, Cheltenham", "192 High Street, Cheltenham", "Pilgrove Farm, Hayden Hill, Cheltenham", "c/o Mr G Fluck, Pilgrove Farm, Hayden Hill, Cheltenham, Gloucestershire"],
# 		"14": ["14 Montpellier Grove, Cheltenham, Gloucestershire", "The Laurels, Charlton Kings, Cheltenham", "The Laurels, London Road, Charlton Kings", "The Laurels, London Road"],
# 		"15": ["Withy Bridge Farm, Boddington, Near Cheltenham, Gloucestershire", "Mill House Farm, Boddington, Near Cheltenham", "Withybridge Farm, Boddington", "Withy Bridge Farm, Boddington, Near Cheltenham, Gloucestershire"],
# 		"16": ["Barrow Hill Farm, Boddington, Cheltenham, Gloucestershire", "Barrow Hill Farm, Boddington, Cheltenham", "Barrow Hill Farm, Boddington", "Barrow Hill Farm, Boddington, Cheltenham, Gloucestershire"],
# 		"18": ["Brookes Laymes Farm, Boddington, Gloucestershire", "Brooklaines Farm, Boddington, Cheltenham", "Brookes Laymes Farm, Boddington", "Brookes Laymes Farm, Boddington, Gloucestershire"],
# 		"19": ["Boddington, Gloucestershire", "Brooklaines Farm, Boddington, Cheltenham", "Boddington", "Boddington, Gloucestershire"],
# 		"20": ["Hayden Farm, Boddington, Near Cheltenham, Gloucestershire", "Hayden Farm, Hayden, Cheltenham", "Hayden Farm, Boddington", "Hayden Farm, Boddington, Near Cheltenham, Gloucestershire"],
# 		"22": ["Wilkins Farm, Barrow, Boddington, Cheltenham, Gloucestershire", "Wilkins Farm, Boddington, Cheltenham", "Wilkins Farm, Barrow, Boddington", "Wilkins Farm, Barrow, Boddington, Cheltenham, Gloucestershire"],
# 		"31": ["1 Hayden Hill Villas, Hayden Hill, Boddington, Cheltenham, Gloucestershire", "1 Hayden Hill Villas, Hayden Hill, Boddington", "Hayden Hill Villas, Hayden Hill, Boddington, Cheltenham, Gloucestershire"],
# 		"33": ["Pilgrove, Hayden Hill, Near Cheltenham, Gloucestershire", "Pilgrove, Hayden Hill, Boddington, Gloucestershire", "Pilgrove, Hayden Hill, Cheltenham", "Pilgrove, Hayden Hilll, Near Cheltenham, Gloucestershire"],
# 		})


