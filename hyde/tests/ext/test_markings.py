# -*- coding: utf-8 -*-
"""
Use nose
`$ pip install nose`
`$ nosetests`
"""
from hyde.fs import File, Folder
from hyde.generator import Generator
from hyde.site import Site

from pyquery import PyQuery

TEST_SITE = File(__file__).parent.parent.child_folder('_test')


class TestMarkings(object):

    def setUp(self):
        TEST_SITE.make()
        TEST_SITE.parent.child_folder(
                    'sites/test_jinja').copy_contents_to(TEST_SITE)

    def tearDown(self):
        TEST_SITE.delete()

    def test_markings(self):
        text = u"""
===
is_processable: False
===
{% filter markdown|typogrify %}
§§ heading
This is a heading
=================
§§ heading.

§§ content
Hyde & Jinja.
§§ .

{% endfilter %}
"""

        text2 = """
{% refer to "inc.md" as inc %}
{% filter markdown|typogrify %}
{{ inc.heading }}
{{ inc.content }}
{% endfilter %}
"""
        site = Site(TEST_SITE)
        site.config.plugins = [
            'hyde.ext.plugins.meta.MetaPlugin',
            'hyde.ext.plugins.markings.MarkingsPlugin']
        inc = File(TEST_SITE.child('content/inc.md'))
        inc.write(text)
        site.load()
        gen = Generator(site)
        gen.load_template_if_needed()
        template = gen.template
        html = template.render(text2, {}).strip()
        assert html
        q = PyQuery(html)
        assert "is_processable" not in html
        assert "This is a" in q("h1").text()
        assert "heading" in q("h1").text()
        assert q(".amp").length == 1
        assert "mark" not in html
        assert "reference" not in html