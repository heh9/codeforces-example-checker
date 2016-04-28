import os, sys, urllib, re, subprocess
from bs4 import BeautifulSoup

def get_problem_link(f):
	with open(f, 'r') as infile:
		return infile.readline()[2:]

def convert_gt_lt(string):
	string = string.replace('&lt;', '<')
	string = string.replace('&gt;', '>')
	return string

def main(soup):
	s_inputs = soup.find_all('div', attrs = {"class" : "input"})
	s_outputs = soup.find_all('div', attrs = {"class" : "output"})
	outs = []
	t_nr = 0

	for sr_input, sr_output in zip(s_inputs, s_outputs):
		t_nr += 1
		_input = sr_input.find_all('pre')
		_output = sr_output.find_all('pre')

		pat = r"\>(.+?)\<"

		input_match = re.findall(pat, str(_input))
		output_match = re.findall(pat, str(_output))
		p = subprocess.Popen(["./" + file_to_compile[:-4]], stdin=subprocess.PIPE,
						 	 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		i_lines = ""
		o_lines = ""
		for line in input_match: i_lines += convert_gt_lt(line) + '\n'
		stdout, stderr = p.communicate(i_lines.encode("utf-8"))
		stdout = stdout.decode("utf-8")
		if len(output_match) > 1: 
			for line in output_match: o_lines += line + '\n'
		else: o_lines = output_match[0]
		if (o_lines == stdout):
			print(80 * '-')
			print ("Test " + str(t_nr) + ": [OK]")
		else: 
			print(80 * '-')
			print("Test " + str(t_nr) + ": [X]\n" + "Input:\n" + i_lines +
				  "Your answer:\n" + stdout + "\nExpected answer:\n" + o_lines)

file_to_compile = sys.argv[1]
problem_link = get_problem_link(file_to_compile)

web_page = urllib.request.urlopen(problem_link)
soup_page = BeautifulSoup(web_page, "html.parser")

subprocess.call(["g++", file_to_compile, "-o", file_to_compile[:-4]])
main(soup_page)
