import re
import random
import sys

from urllib.request import urlopen
from bs4 import BeautifulSoup

def extract_words(s):
	""" Simple tokenizer extracting words using regex
		excluding digits
	"""

	words = re.findall(r"[^\d\W]+", s)
	return words


def wiki_scrape(lang="en", tokenizer=extract_words, p_total=100, p_page=200):
	""" Creates a corpus of paragraphs from random Wikipedia articles
		given a language | lang
			  a number of paragraphs | p_total
			  a limit to the number of paragraphs pr. article | p_page
			  and a tokenizer | tokenizer
	"""
	corpus = []
	n=0

	print()
	print("Initializing scraping {l}-corpus of {p} paragraphs".format(l=lang, p=p_total))

	msg = "Number of pages read: {n} \t corpus size: {s}\r "
	sys.stdout.write(msg.format(n=n, s=len(corpus)))
	sys.stdout.flush()

	query = "https://{}.wikipedia.org/wiki/Special:Random".format(lang)

	while len(corpus)<p_total:
		n+=1
		
		html = urlopen(query)
		soup = BeautifulSoup(html, features="html.parser")

		paragraphs = soup.findAll("p")

		to_load = p_page-((len(corpus)+p_page)-p_total)
		
		if to_load < len(paragraphs):	
			sample = random.sample(range(0, len(paragraphs)), to_load)
		else:
			sample = range(0, len(paragraphs))

		for i in sample:
			p_text = paragraphs[i].getText()
			words = tokenizer(p_text)
			if words: corpus.append(words)

		sys.stdout.write(msg.format(n=n, s=len(corpus)))
		sys.stdout.flush()			

	random.shuffle(corpus)
	print("\n Done!")

	return corpus


if __name__ == "__main__":
	languages = sys.argv[1:-1]
	n_par = int(sys.argv[-1])

	for lang in languages:
		paragraphs = wiki_scrape(lang=lang, p_total=n_par)

		with open("resources/wiki_{}.txt".format(lang), "w") as f:
			for p in paragraphs:
				f.write(" ".join(p)+"\n")