import pytest

from ssllabsscan.report_template import REPORT_HTML


class TestReportTemplate:
    """Test cases for report_template module."""

    def test_report_html_template_structure(self):
        """Test that the HTML template has the expected structure."""
        assert isinstance(REPORT_HTML, str)
        assert len(REPORT_HTML) > 0

    def test_report_html_contains_doctype(self):
        """Test that the template contains proper HTML5 doctype."""
        assert "<!DOCTYPE html>" in REPORT_HTML

    def test_report_html_contains_html_tag(self):
        """Test that the template contains html tag."""
        assert "<html lang=\"en\">" in REPORT_HTML

    def test_report_html_contains_head_section(self):
        """Test that the template contains head section with meta charset."""
        assert "<head>" in REPORT_HTML
        assert "<meta charset=\"UTF-8\">" in REPORT_HTML

    def test_report_html_contains_title_placeholder(self):
        """Test that the template contains title placeholder."""
        assert "{{VAR_TITLE}}" in REPORT_HTML
        assert "<title>{{VAR_TITLE}}</title>" in REPORT_HTML

    def test_report_html_contains_css_link(self):
        """Test that the template contains CSS stylesheet link."""
        assert '<link rel="stylesheet" href="styles.css">' in REPORT_HTML

    def test_report_html_contains_body_structure(self):
        """Test that the template contains proper body structure."""
        assert "<body>" in REPORT_HTML
        assert "<h1>{{VAR_TITLE}}</h1>" in REPORT_HTML

    def test_report_html_contains_table_structure(self):
        """Test that the template contains table structure."""
        assert '<table class="tftable" border="1">' in REPORT_HTML
        assert "{{VAR_DATA}}" in REPORT_HTML

    def test_report_html_contains_closing_tags(self):
        """Test that the template contains proper closing tags."""
        assert "</table>" in REPORT_HTML
        assert "</body>" in REPORT_HTML
        assert "</html>" in REPORT_HTML

    def test_report_html_template_placeholders(self):
        """Test that the template contains expected placeholders."""
        # Count occurrences of placeholders
        title_count = REPORT_HTML.count("{{VAR_TITLE}}")
        data_count = REPORT_HTML.count("{{VAR_DATA}}")

        assert title_count == 2  # Once in title, once in h1
        assert data_count == 1   # Once in table

    def test_report_html_is_valid_template(self):
        """Test that the template can be used for string formatting."""
        # Test that we can replace the placeholders
        test_title = "Test SSL Report"
        test_data = "<tr><td>Test Data</td></tr>"

        formatted_html = REPORT_HTML.replace("{{VAR_TITLE}}", test_title)
        formatted_html = formatted_html.replace("{{VAR_DATA}}", test_data)

        assert test_title in formatted_html
        assert test_data in formatted_html
        assert "{{VAR_TITLE}}" not in formatted_html
        assert "{{VAR_DATA}}" not in formatted_html

    def test_report_html_contains_expected_classes(self):
        """Test that the template contains expected CSS classes."""
        assert 'class="tftable"' in REPORT_HTML

    def test_report_html_contains_expected_attributes(self):
        """Test that the template contains expected HTML attributes."""
        assert 'border="1"' in REPORT_HTML
        assert 'lang="en"' in REPORT_HTML
        assert 'charset="UTF-8"' in REPORT_HTML

