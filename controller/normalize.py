class Normalize(object) :
	def sign_converter(word):
	    word_dict = {
	        '“' : "",
	        ',' : "",
	        '.' : "",
	        ':' : "",
	        '—' : "",
	        '“' : "",
	        "?" : ""
	    }
	    res = ""
	    for letter in word:
	        if letter in word_dict:
	            res += word_dict[letter]
	        else:
	            res += letter
	    return res

	def number_converter(word):
	    word_dict = {
	        '!' : "1",
	        'l' : "1",
	        'L' : "1",
	        'O' : "0",
	        'o' : "0",
	        '?' : "7",
	        'B' : "8",
	        'S' : "5",
	        'D' : "0",
	        ':' : "",
			't' : "1",
			'g' : "9"
	    }
	    res = ""
	    for letter in word:
	        if letter in word_dict:
	            res += word_dict[letter]
	        else:
	            res += letter
	    return res

	def letter_converter(word):
	    word_dict = {
	        '4' : "A",
	        '8' : "B",
	        '3' : "E",
	        '6' : "G",
	        '1' : "I",
	        'i' : "I",
	        '7' : "J",
	        '0' : "O",
	        '5' : "S",
	        ':' : "",
	        ',' : "",
	        "." : "",
			'w' : "W",
			"c" : "C",
			"f" : "F", 
			"j" : "J",
			"k" : "K",
			"o" : "O",
			"p" : "P",
			"s" : "S",
			"u" : "U", 
			"v" : "V",
			"x" : "X", 
			"z" : "Z"
	    }
	    res = ""
	    for letter in word:
	        if letter in word_dict:
	            res += word_dict[letter]
	        else:
	            res += letter
	    return res

	def sim_converter(word):
	    word_dict = {
	        '1' : "",
			'2' : "",
			'3' : "",
			'4' : "",
			'5' : "",
			'6' : "", 
	        ',' : "",
	        "." : ""
	    }
	    res = ""
	    for letter in word:
	        if letter in word_dict:
	            res += word_dict[letter]
	        else:
	            res += letter
	    return res