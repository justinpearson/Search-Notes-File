from lib import parse_notes_file_into_entries

from io import StringIO
from textwrap import dedent
from pprint import pprint as pp

def test_normal_case():
	assert parse_notes_file_into_entries( StringIO( dedent( 
		'''\
		This non-entry text at the very top of the file should get thrown away.

		2020-01-01
		First entry title
		
		When in the course of human events,
		it becomes necessary for one people to dissolve 
		the political bands which have connected them with another,
		
		and so on.

		2020-02-02
		Second entry
		Just a quick note.

		'''))) == [
		{
			'date': '2020-01-01'
		,	'title': 'First entry title'
		,	'body': [
				'',
				'When in the course of human events,',
				'it becomes necessary for one people to dissolve ',
				'the political bands which have connected them with another,',
				'',
				'and so on.',
				''
				]
		,	'line number': 1
		},
		{
			'date': '2020-02-02'
		,	'title': 'Second entry'
		,	'body': ['Just a quick note.','']
		,	'line number': 10
		},
		]

def test_date_formats():
	es = parse_notes_file_into_entries( StringIO( dedent( '''\
		~~2020-01-01
		20200202
		2020.02.02
		2020-03-03
		''')))

	assert es[0]['date'] == '~~2020-01-01'
	assert es[1]['date'] == '20200202'
	assert es[2]['date'] == '2020.02.02'
	assert es[3]['date'] == '2020-03-03'

def test_empty_title_ok():
	s = StringIO(dedent('''\
				2020-03-03

				^-- Empty title is ok!
				''')
			)
	es = parse_notes_file_into_entries(s)
	assert es[0]['title'] == ''


def test_empty_body_ok():
	s = StringIO(dedent('''\
				2020-01-02
				title 1
				2020-01-03
				title 2
				body 2
				'''))
	es = parse_notes_file_into_entries(s)
	assert es[0]['body'] == []

def test_date_must_be_indented():
	# An entry's date must begin at the start of the line.
	# This prevents you from accidentally making a new entry.
	
	# Here, the 2nd entry's indented date causes it to be counted
	# as the 1st entry's body:
	s = StringIO(dedent('''\
				2020-01-02
				title 1
				body 1
				 2020-01-03
				title 2
				body 2
				'''))
	es = parse_notes_file_into_entries(s)
	assert es[0]['body'] == [ 'body 1'
							, ' 2020-01-03'
							, 'title 2'
							, 'body 2'
							]














