import matplotlib.pyplot as plt
from collections import Counter, defaultdict

from scipy.interpolate import make_interp_spline, BSpline
import numpy as np


def plot_freq_distr(sample_list, language_list, rel_freq=False, interpolate=(2, 300), most_common=30, sort_by_freq=False):
	""" Plots a frequency distribution over the most common elements
		from a number of language samples
		given a list of samples   | sample_list
		      a list of languages | languages_list
		      whether relative frequency is used    | rel_freq
		      whether the frequency is interpolated | interpolate
		      the number of most common elements included | most_common
		      by the freq of which language (if any) the distribution is sorted | sort_by_freq
	"""

	lang_dict = defaultdict(dict)
	index = set()

	# Create freq distr and index
	for lang, sample in zip(language_list, sample_list):
		lang_dict[lang]["c_dict"] = Counter(sample)

		lang_dict[lang]["most_common"] = lang_dict[lang]["c_dict"].most_common(most_common)

		index |= set([elem for elem, c in lang_dict[lang]["most_common"]]) # Update index
	
	# Sort index
	if sort_by_freq in lang_dict:
		index = sorted(index, key=lambda x:lang_dict[sort_by_freq]["c_dict"][x], reverse=True)
	else:
		index = sorted(index)

	# Get distr by index
	for lang in lang_dict:
		lang_dict[lang]["distr"] =[lang_dict[lang]["c_dict"].get(seq, 0) for seq in index]


	# Plot
	for i, lang in enumerate(lang_dict):

		if rel_freq:
			total_counts = sum(lang_dict[lang]["c_dict"].values())
			y = [count/total_counts for count in lang_dict[lang]["distr"]]
			lang_dict[lang]["rel_freq"] = y

		else:
			y = lang_dict[lang]["distr"]
	
		if interpolate:
			x_new = np.linspace(0, len(index), interpolate[-1])
			spl = make_interp_spline(list(range(0, len(index))), y, interpolate[0])
			y_new = spl(x_new)
			lang_dict[lang]["interpol"] = (x_new, y_new)
			plt.plot(x_new, y_new, label=lang)
		else:
			plt.bar(range(0, len(index)), y, label=lang, align= "edge" if (i == 0 and len(lang_dict)>1) else "center")


	plt.legend()
	plt.xticks(range(len(index)), ["".join(elem) for elem in index])
	_, _, ymin, ymax = plt.axis()
	margin=0.5 if interpolate else 1
	plt.axis([-margin, len(index)-1+margin, ymin, ymax])

	plt.show()

	return lang_dict