from freq_analysis import plot_freq_distr

def extract_ngrams(seq, n):
	""" Return list of n-grams given sequence (list, tuble, string)
		Fails if n > len(seq)
	"""
	return list(zip(*[seq[x:] for x in range(n)]))

if __name__ == "__main__":
	languages = ["da", "no", "sv"]
	ngrams = []
	n = 2

	for lang in languages:

		with open("resources/wiki_{}.txt".format(lang)) as f:
			paragraphs = [line.strip() for line in f.readlines()]

		ngrams.append([])
		# Extract character n-grams pr word
		for p in paragraphs:
			for word in p.split():
				ngrams[-1].extend(extract_ngrams(word.lower(), n))

	plot_freq_distr(ngrams, languages, rel_freq=True, interpolate=(2,300), sort_by_freq=False, most_common=10)