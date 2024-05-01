import pytest
from tdi_rust_python_tools import strip_html_tags

from remove_html import strip_html_tags_python


@pytest.mark.parametrize(
    argnames=("value",),
    argvalues=(
        ("",),
        ("Normal text with no html tags",),
        ("N/A",),
        ("<p>Some text</p>",),
        ("<div>More text</div>",),
        ("<span>Even more text</span>",),
        ("<p>Text with < symbol</p>",),
        ("<div>Text with > symbol</div>",),
        ("<span>Text with < and > symbols</span>",),
        ("Lovely long text with no html tags",),
        ("<div>",),
        ("<p><span>Text with nested tags</span></p>",),
        ("<p>Text with <span>tags</span></p>",),
        (
            'Please <a href="http://www.biorbyt.com/contact-us/" target="_blank" rel="nofollow">contact us for the exact immunogen sequence. The peptide is available as <a href="http://www.biorbyt.com/hoxa10-peptide-orb394006 target=_blank" rel="nofolow">orb394006.',
        ),
    ),
)
def test_clean_values_1(value: str) -> None:
    assert strip_html_tags(value) == strip_html_tags_python(value)
