import pytest
import helpers as h
import wikipedia as wiki



def get_wiki_links(page_name):
    try:
        test_page = wiki.page(page_name)
        return test_page.links
    except wiki.DisambiguationError as e:
        return e.options
    except wiki.PageError:
        return []


test_titles = [
    ("Mars (Planet)"), # Basic long page to check
    ("Mars (disambiguation)"),  # Check Disambiguation pages
    ("Head of navigation"),  # Check article stubs
    ("Mars (1997 film)") # Check and empty page
]

test_disam = [
    ("Mars(Planet)"), # Basic long page to check
    ("Mars (disambiguation)"),  # Check Disambiguation pages
    ("Head of navigation")  # Check article stubs
]

test_disam = [
    ("Mars (Planet)", False), # Basic long page to check
    ("Mars (disambiguation)", True),  # Check Disambiguation pages
    ("Head of navigation", False),  # Check article stubs
    ("Mars (1997 film)", False) # Check and empty page
]

test_page = [
    ("Mars (Planet)", ), # Basic long page to check
    ("Mars (disambiguation)", ),  # Check Disambiguation pages
    ("Head of navigation", ),  # Check article stubs
    ("Mars (1997 film)", ) # Check and empty page
]

test_stored = [
    ("Mars (Planet)", True ), # Basic long page to check
    ("Mars (disambiguation)", False),  # Check Disambiguation pages
    ("Head of navigation", True),  # Check article stubs
    ("Mars (1997 film)", False) # Check and empty page
]


@pytest.mark.parametrize("page_name", test_titles)
def test_get_links(page_name):
        assert len(h.get_links(page_name)) <= len(get_wiki_links(page_name))

@pytest.mark.parametrize("page_name, bool_check", test_disam)
def test_is_disamb(page_name, bool_check):
        assert h.is_disamb(page_name) is bool_check

@pytest.mark.parametrize("page_name, bool_check", test_page)
def test_is_page(page_name, bool_check):
        assert h.is_page(page_name) is bool_check

@pytest.mark.parametrize("page_name", test_titles)
def test_read_links(page_name):
        assert len(h.read_links(page_name)) == len(h.get_links(page_name))

@pytest.mark.parametrize("page_name, bool_check", test_stored)
def test_is_stored(page_name, bool_check):
        assert h.is_stored(page_name) is bool_check
