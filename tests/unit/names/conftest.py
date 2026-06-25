import pytest


@pytest.fixture()
def names():
	return [
		{
			'final': "K/Katharine/H Duncombe or K (Katharine)/H Duncombe",
			'original': [
				"Katharine Duncombe","H Duncombe",
				"K Duncombe",
			],
		},
		{
			'final': "Messrs H/Herbert Jones and H Jones or Messrs H (Herbert) Jones and H Jones  ",
			'original': [
				"H Jones and H Jones","Messrs H Jones and H Jones",
				"H Jones and H Jones",
				"Mr Herbert Jones and H Jones",
			],
		},
		{
			'final': "John R S Rippin",
			'original': [
				"John R S Rippin","J R S Rippin",
				"J R S Rippin",
			],
		},

	]


@pytest.fixture()
def names1():
	return({
        "1": ["H Arkell", "H Arkell", "H Arkell", "H Arkell"], 
		"2": ["", "W H Buckle", "W H Buckle", "W H Buckle"], 
		"3": ["R A Burroghs", "R Burroughs", "R Burroughs", "R Burroughs"],
		"6": ["A E Cook", "A E Cook", "A E Cook", "A E Cook"],
		"7": ["A G Griffiths", "W L Edmunds", "W L Edmunds", "W L Edmunds"],
		"9": ["E Stacey", "A G Cooper bailiff for J S Gibbons Esq", "A G Cooper (bailiff to J S Gibbons)", "A G Cooper bailiff for J S Gibbons Esq"],
		"10": ["", "F W Hinton", "", "F W Hinton"],
		"14": ["G P Rymer", "G P Rymer", "G P Rymer", "G P Rymer"],
		"15": ["A Spragg", "A Spragg", "A Spragg", "A Spragg"],
		"16": ["H Bowl", "Harry Bowl", "H Bowl", "Harry Bowl"],
		"18": ["A Tombs", "A Tombs", "A Tombs", "A Tombs"],
		"19": ["C Tombs", "C Toombs", "C Toombs", "C Toombs"],
		"20": ["G O Tombs", "G O Tombs", "G O Tombs", "G O Tombs"],
		"22": ["G Wilkins", "G Wilkins", "Geo Wilkin", "G Wilkins"],
		"31": ["", "F Bendall", "F Bendall", "F Bendall"],
		"33": ["F Thomas", "Frank Thomas", "F. Thomas", "Frank Thomas"]
         })


@pytest.fixture()
def names2():
	return({
		"1": ["R A Burroghs", "R Burroughs", "R Burroughs", "R Burroughs"],
		"2": ["R Burroughs", "R Burroughs", "R Burroughs", "R Burroughs"],
		"3": ["R Burroghs", "R Burroughs", "R Burroughs", "R Burroughs"],
		"4": ["R Burroughs", "J Burroghs", "J Burroughs", "R Burroughs"], 
		"5": ["R J Burroghs", "J Burroughs", "J Burroughs", "J Burroughs"],
		"6": ["J R Burroghs", "J Burroughs", "J Burroughs", "J Burroughs"], 
		"7": ["J R Burrows", "J Burroughs", "J Burroughs", "J Burroughs"], 
		"8": ["R J Burroughs", "R L Burroughs", "R Burroughs", "R Burroughs"],
		"9": ["R J Burrows", "R L Burroughs", "J Burroughs", "J Burroughs"],
		"10": ["R J Burrows", "R L Burroughs", "R Burroughs", "R Burroughs"],
		"11": ["R Burrows", "R Burroughs", "R Burroughs", "F Rymer"],
		"12": ["R Burrows", "R Burroughs", "R Burroughs", "R Rymer"],
		"13": ["R Burrows", "F Burroughs", "R Burroughs", "F Rymer"],
		"14": ["R Burrows", "R F Burroughs", "R Burroughs", "F Rymer"],
		"15": ["R J Burrows", "F Burroughs", "R Burroughs", "F Rymer"],
		"16": ["R J Burrows", "R Burroughs", "R Burroughs", "R J Burroghs"],
		"17": ["R J Burrows", "A E Cook", "G P Rymer", "Geo Wilkin"],
		"18": ["R J Burrows", "R Burroughs", "G P Rymer", "Geo Wilkin"],
		"19": ["R J Burrows", "R Burroughs", "R Burroghs", "R J Burroghs"],
		"20": ["E Stacey", "A G Cooper bailiff for J S Gibbons Esq", "A G Cooper (bailiff to J S Gibbons)", "A G Cooper bailiff for J S Gibbons Esq"]                
        })


@pytest.fixture()
def names3():
	return({"1": ["Messrs Rowe and Raddy", "Mr A C Raddy for Rowe and Raddy"]})
