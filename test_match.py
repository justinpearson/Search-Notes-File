from lib import entry_matchesQ

from dataclasses import dataclass, field

@dataclass
class DummyArgs:
	title_search_strs : list = field(default_factory=list)
	body_search_strs : list = field(default_factory=list)
	match_ANY_title : bool = False
	match_ANY_body : bool = False
	match_title_OR_body : bool = False

def test_search_is_case_insensitive():
	e = { 'title': 'List Of Apples', 'body': ['Red','Green','...'] }
	a = DummyArgs( title_search_strs = ['apple'] )
	assert entry_matchesQ(e, a)

def test_search_for_str_in_title_not_the_other_way_around():
	e = { 'title': 'List Of Apples', 'body': ['Red','Green','...'] }
	a = DummyArgs( title_search_strs = ['zapple'] )
	assert not entry_matchesQ(e, a)

def test_regex():
	es_match = [ { 'title': 'How MPEG compression works', 'body': [] }
			   , { 'title': 'My cars MPG sucks', 'body': [] }
			   , { 'title': 'File.mpg', 'body': [] }
			   , { 'title': 'File.mpeg', 'body': [] }
			   ]
	es_no_match = [ { 'title': 'Cat', 'body': [] }
				  , { 'title': 'Dog', 'body': [] }
				  ]
	a = DummyArgs( title_search_strs = [r'mpe?g'] )
	for e in es_match:
		assert entry_matchesQ(e, a)
	for e in es_no_match:
		assert not entry_matchesQ(e, a)

def test_match_ALL_title_strings():
	e1 = { 'title': 'List of apples', 'body': [] }
	e2 = { 'title': 'List of poems', 'body': [] }

	a = DummyArgs( title_search_strs = ['list'] )
	assert entry_matchesQ(e1, a)
	assert entry_matchesQ(e2, a)

	a = DummyArgs( title_search_strs = ['apple', 'list'] )
	assert entry_matchesQ(e1, a)
	assert not entry_matchesQ(e2, a)

def test_match_ANY_title_string():
	e1 = { 'title': 'List of apples', 'body': [] }
	e2 = { 'title': 'List of poems', 'body': [] }

	a = DummyArgs( title_search_strs = ['apple', 'list']
				 , match_ANY_title = True
				 )
	assert entry_matchesQ(e1, a)
	assert entry_matchesQ(e2, a)

def test_match_ALL_body_strings():
	e1 = {'title': '', 'body': ['aaa bbb', 'ccc']}
	e2 = {'title': '', 'body': ['aaa','bbb']}
	a = DummyArgs( body_search_strs = ['aaa','bbb','ccc'] )
	assert entry_matchesQ(e1, a)
	assert not entry_matchesQ(e2, a)

def test_match_ANY_body_string():
	e = {'title': '', 'body': ['aaa','bbb']}

	a = DummyArgs( body_search_strs = ['aaa','bbb','ccc'] )
	assert not entry_matchesQ(e, a)

	a.match_ANY_body = True
	assert entry_matchesQ(e, a)

def test_match_title_OR_body():
	e = {'title': 'aaa', 'body': ['bbb ccc', 'ddd']}

	a = DummyArgs( title_search_strs = ['xxx'], body_search_strs = ['ddd'] )
	assert not entry_matchesQ( e, a )

	a.match_title_OR_body = True
	assert entry_matchesQ(e, a)

