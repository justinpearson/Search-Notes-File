import re, sys, os

################################
# Timing convenience function.
################################

from timeit import default_timer as timer

class TimePrinter:
	def __init__(self):
		self.tstart = timer()
	def p(self,s):
		tend = timer()
		print(f'{round(1000*(tend-self.tstart))} ms - {s}')
		self.tstart = tend
	def reset(self):
		self.tstart = timer()

##################################
# Parse args
##################################

def parse_args():

	SUBLIME_EXE = "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl"
	NOTES_FILE = '/Users/justin/Notes/notes.txt'

	import argparse
	parser = argparse.ArgumentParser(description='Search my notes file and prompt to open a matching entry in Sublime Text.')

	parser.add_argument('title_search_strs', nargs='*', default=[], help="Strings to search the entries' titles for.")
	# Note: wanted title_search_strs to have metavar=('S1','S2'), but looks like a long-standing bug in argparse:
	# https://stackoverflow.com/questions/7953623/how-to-modify-the-metavar-for-a-positional-argument-in-pythons-argparse
	# https://bugs.python.org/issue14074
	parser.add_argument('-b','--body-search-strs', metavar=('S1','S2'), nargs='*', help="Strings to search the entries bodies for. (Not req'd.)", default=[])
	parser.add_argument('-v', '--verbose', default=False, help='Print helpful debugging info.', action='store_true')
	parser.add_argument('--sublime-exe', metavar='PATH', help='Path to Sublime Text executable.', default=SUBLIME_EXE)
	parser.add_argument('--notes-file', metavar='PATH', help='Path to my notes file.', default=NOTES_FILE)
	parser.add_argument("--match-ANY-title", action="store_true", default=False, help="Matching entries' titles must have AT LEAST 1 given title str present. (Default is ALL.)")
	parser.add_argument("--match-ANY-body", action="store_true", default=False, help="Matching entries' bodies must have AT LEAST 1 given body str present. (Default is ALL.)")
	parser.add_argument("--match-title-OR-body", action="store_true", default=False, help="Entry matches if its title OR body matches the given search terms. (Default is title AND body must match.)")

	args = parser.parse_args()

	if args.verbose:
		print('~~~~~~~~~~~~ BEGIN ARGS ~~~~~~~~~~~~~')
		print(args)
		print('~~~~~~~~ END ARGS ~~~~~~~~~~~~~')

	if args.title_search_strs == [] and args.body_search_strs == []:
		parser.print_help()
		print('You gave:')
		print(args)
		raise ValueError('Expected >=1 title or body search str!')

	return args

###################################
# Verify you have Sublime Text & a Notes file.
###################################

def verify_subl(sublime_exe):
	if not (os.path.isfile(sublime_exe) and os.access(sublime_exe, os.X_OK)):
		print(f'''
			Sublime Text executable not found, or not executable! Exiting.
			(I was looking for "{sublime_exe}")
			''')
		exit(1)
	else:
		print(f'Found subl = {sublime_exe}')

def verify_notes(notes_file):
	if not os.path.isfile(notes_file):
		print(f'''
			Can't find notes file "{notes_file}", exiting!
			(I was looking in my pwd, "{os.getcwd()}".)
			''')
		exit(1)
	else:
		print(f'Found notes file = {notes_file}')

##########################################
# Parse entries
##########################################

def parse_notes_file_into_entries(notes_file):

	from itertools import accumulate
	from more_itertools import split_before

	# An entry begins with a line that has the entry's date:

	date_patt = re.compile(r'^~?~?\d{4}[-.]?\d{2}[-.]?\d{2}\W*$')
	# Explanation: 
	#   ^ beginning of line
	#   ~?~? my dates used to be like ~~2015.03.18, but later I left off the ~~
	#   [-.]? I've used 20150318 2015.03.18 2015-03-18
	#   \W*  only non-word chars on the rest of the line, plz (to catch ONLY lines with this type of date)
	#   $ end of line.

	tprint = TimePrinter()
	lines = notes_file.read().splitlines()
	tprint.p(f'Read notes file: {len(lines)} lines.')

	# Split when you see a line that's just a date:
	entry_line_lists = list(split_before(lines, lambda l: date_patt.match(l)))

	# If the notes file started with some random text (not a date),
	# the first entry_line_list will not actually be a real entry. Delete it.
	if not date_patt.match(entry_line_lists[0][0]):
		del entry_line_lists[0]

	tprint.p(f'Split into {len(entry_line_lists)} entries.')

	# Compute the line number of each entry.
	entry_line_ends = list(accumulate(map(len, entry_line_lists)))
	entry_line_starts = [1] + [1+n for n in entry_line_ends[:-1]] # subl uses 1-indexed line numbers

	entries = [
		{ 'line number': line_num
		, 'date': entry_lines[0]
		, 'title': entry_lines[1] if len(entry_lines)>1 else '' # for corner-cases where 2 dates appear on 2 adjacent lines
		, 'body': entry_lines[2:] if len(entry_lines)>2 else []
		} 
		for line_num, entry_lines in zip(entry_line_starts, entry_line_lists)
		]

	tprint.p(f'Parsed {len(entries)} entries.')

	return entries

##########################################
# Search entries
##########################################

def entry_matchesQ(entry, args):
	# Note that search strs can be regexs.

	# Compute whether the entry's title matches the title search strings,
	# and whether the entry's body matches the body search strings,
	# using all() by default, or any() if the user passed args.match_ANY_title
	# or args.match_ANY_body.
	title_matchesQ, body_matchesQ = [
		(any if use_anyQ else all)(re.compile(s, re.IGNORECASE).search(text) for s in search_terms)
		for text, search_terms, use_anyQ in zip( [entry['title'], ' '.join(entry['body'])]
											  , [args.title_search_strs, args.body_search_strs]
											  , [args.match_ANY_title, args.match_ANY_body]
											  )
		]

	# The entry matches if its title matches AND its body matches;
	# the user can pass args.match_title_OR_body to use OR instead of AND.
	return title_matchesQ or body_matchesQ if args.match_title_OR_body else title_matchesQ and body_matchesQ

############################################
# Ask user which entry to open
############################################

def pick_idx_of_result_to_open(num_results):

	if num_results > 1: # normal case
		s = input('Which entry? (leave blank to quit): ').strip()
		if s == '':
			print('Ok, quitting!')
			exit(0)

	elif num_results == 1:
		# Only 1 result, I shouldn't have to enter '0'.
		s = input('Only 1 result, will open it. Enter to continue. Any other char to quit.')
		if s != '':
			print('Ok, quitting!')
			exit(0)
		s = '0'

	if not re.match(r'\d+',s):
		print(f'Expected a number, not "{s}", quitting.')
		exit(1)

	return int(s)
