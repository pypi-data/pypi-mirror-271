words_that_are_bad = (
	'FUCK',
	'CUNT',
	'WANK',
	'WANG',
	'PISS',
	'COCK',
	'SHIT',
	'TWAT',
	'TITS',
	'FART',
	'HELL',
	'MUFF',
	'DICK',
	'KNOB',
	'ARSE',
	'SHAG',
	'TOSS',
	'SLUT',
	'TURD',
	'SLAG',
	'CRAP',
	'POOP',
	'BUTT',
	'FECK',
	'BOOB',
	'JISM',
	'JIZZ',
	'PHAT',
)

bad_words = []

for word in words_that_are_bad:
	bad_words.append(word)
	bad_words.append(word.replace('0', '0'))
	bad_words.append(word.replace('I', '1'))
	bad_words.append(word.replace('Z', '2'))
	bad_words.append(word.replace('S', '5'))
