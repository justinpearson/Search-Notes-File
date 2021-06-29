from lib import entry_matchesQ

from dataclasses import dataclass, field

@dataclass
class DummyArgs:
	title_search_strs : list = field(default_factory=list)
	body_search_strs : list = field(default_factory=list)
	match_ANY_title : bool = False
	match_ANY_body : bool = False 
	match_title_OR_body : bool = False

from pytest import fixture
from io import StringIO
from textwrap import dedent
from lib import parse_notes_file_into_entries

@fixture
def entries():
	return parse_notes_file_into_entries( StringIO( dedent( '''\
		2020-01-01
		List Of Apples

		- Red delicious: too mealy
		- Gravenstein: can't remember
		- Granny smith: too tart
		- Gala: too small
		- Honeycrisp: too expensive


		2020-02-02
		List of chapter intros of Pride and Prejudice

		Chapter 1 It is a truth universally acknowledged,
		that a single man in possession of a good fortune, 
		must be in want of a wife. 

		Chapter 2 ...
		''')))

@fixture
def entry_apples(entries):
	return entries[0]

@fixture
def entry_book(entries):
	return entries[1]	


def test_search_is_case_insensitive(entry_apples):
	a = DummyArgs( title_search_strs = ['apple'] )
	b = DummyArgs( title_search_strs = ['zapple'] )
	assert entry_matchesQ(entry_apples, a)
	assert not entry_matchesQ(entry_apples, b)


def test_regex(entry_apples, entry_book):
	a = DummyArgs( title_search_strs = [r'\bof\b'] )
	assert entry_matchesQ(entry_apples, a)
	assert entry_matchesQ(entry_book, a)


def test_title_strings(entry_apples, entry_book):
	a = DummyArgs( title_search_strs = ['apple', 'list of'] )
	assert entry_matchesQ(entry_apples, a)
	assert not entry_matchesQ(entry_book, a)

	a = DummyArgs( title_search_strs = ['list of'] )
	assert entry_matchesQ(entry_apples, a)
	assert entry_matchesQ(entry_book, a)


def test_match_ANY_title(entry_apples, entry_book):
	a = DummyArgs( title_search_strs = ['apple', 'list of']
				 , match_ANY_title = True
				 )
	assert entry_matchesQ(entry_apples, a)
	assert entry_matchesQ(entry_book, a)


def test_body_strings(entry_apples, entry_book):
	a = DummyArgs( body_search_strs = ['truth','universally','acknowledged'] )
	assert not entry_matchesQ(entry_apples, a)
	assert entry_matchesQ(entry_book, a)


def test_match_ANY_body(entry_apples, entry_book):
	s = ['falsehood','universally','acknowledged']

	a = DummyArgs( body_search_strs = s )
	assert not entry_matchesQ( entry_book, a )

	b = DummyArgs( body_search_strs = s, match_ANY_body = True ) 
	assert entry_matchesQ( entry_book, b )


def test_match_title_OR_body(entry_apples, entry_book):
	a = DummyArgs( title_search_strs = ['foo'], body_search_strs = ['chapter'] )
	assert not entry_matchesQ( entry_book, a )

	b = DummyArgs( title_search_strs = ['foo'], body_search_strs = ['chapter'], match_title_OR_body = True )
	assert entry_matchesQ(entry_book, b)

