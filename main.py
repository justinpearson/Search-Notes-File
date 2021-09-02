from lib import *

import sys, os

print(f'Hi from "{sys.argv[0]}" !')
print(f'pwd = {os.getcwd()}')

def main():
	args = parse_args()
	verify_subl(args.sublime_exe)
	verify_notes(args.notes_file)

	entries = parse_notes_file_into_entries(open(args.notes_file,'r'))

	tprint = TimePrinter()

	results = [e for e in entries if entry_matchesQ(e, args)]

	tprint.p(f'''{len(results)} results matching: 
		title={args.title_search_strs} 
		body={args.body_search_strs} 
		match_ANY_title={args.match_ANY_title} 
		match_ANY_body={args.match_ANY_body} 
		match_title_OR_body={args.match_title_OR_body}
		''')

	# Bail if no results.
	if len(results) == 0:
		print('0 results, sorry!')
		exit(0)

	# Print results so user can pick one.
	for i,e in enumerate(results):
		print(f"[{i}] {e['line number']}: {e['date']} - {e['title']}")

	n = results[pick_idx_of_result_to_open(len(results))]['line number']

	# TODO: FIX THIS HACK: LINE NUMBERS OFF BC FILE STARTS WITH A NON-ENTRY
	n += 3

	# Open chosen result:
	print(f'Opening notes file in Sublime Text at line {n}...')
	from subprocess import call
	call([
		args.sublime_exe,
		f"{args.notes_file}:{n}"
		])

main()
print(f'Bye from "{sys.argv[0]}" !')