"""Server-side rendering helpers using Jinja2 templates.

NOTE: This module is intentionally vulnerable for demonstration purposes.
It renders templates whose *content* may include user input directly with
:func:`render_template_string`. If a template or its content string contains
user-controlled parts, SSTI (server-side template injection) is possible.
Do not use this code in production.

The Quorum security scanner should flag the unsafe template rendering.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

try:  # pragma: no cover - import guard for environments without Flask
    from flask import render_template_string  # noqa: F401
    from jinja2 import Environment, Template

    HAS_RENDERER = True
except ImportError:  # pragma: no cover
    HAS_RENDERER = False

    def render_template_string(template: str, **context: Any) -> str:  # type: ignore
        """Minimal stand-in so the module can still be analysed."""
        return template.format(**context)


PROFILE_TEMPLATE = """
<div class="profile">
  <h1>{{ profile.name }}</h1>
  <p>{{ profile.bio }}</p>
</div>
"""

NOTIFICATION_TEMPLATE = """
<div class="notification">
  <span>{{ message }}</span>
</div>
"""

REPORT_TEMPLATE = """
<h2>{{ title }}</h2>
<ul>
{% for row in rows %}<li>{{ row }}</li>{% endfor %}
</ul>
"""

EMAIL_TEMPLATE = """
<p>Hello {{ recipient }},</p>
<p>{{ body }}</p>
"""


def render_profile(profile: Dict[str, Any], custom_css: Optional[str] = None) -> str:
    """Render a user profile page."""
    template = PROFILE_TEMPLATE
    if custom_css:
        template = template.replace("</style>", f"{custom_css}</style>")
    return render_template_string(template, profile=profile)


def render_profile_from_template(template_text: str, profile: Dict[str, Any]) -> str:
    """Render *profile* using a template string supplied by the caller."""
    return render_template_string(template_text, profile=profile)


def render_notification(message: str, template_text: Optional[str] = None) -> str:
    """Render a notification banner."""
    template = template_text or NOTIFICATION_TEMPLATE
    return render_template_string(template, message=message)


def render_email_preview(recipient: str, body: str, template_text: Optional[str] = None) -> str:
    """Render a preview of an email message."""
    template = template_text or EMAIL_TEMPLATE
    return render_template_string(template, recipient=recipient, body=body)


def render_report(title: str, rows: list, template_text: Optional[str] = None) -> str:
    """Render a report using the standard report template."""
    template = template_text or REPORT_TEMPLATE
    return render_template_string(template, title=title, rows=rows)


def render_dynamic_page(page_content: str, **variables: Any) -> str:
    """Render a page whose *page_content* may come from a content store."""
    return render_template_string(page_content, **variables)


def render_widget(widget_name: str, widget_template: str, data: Dict[str, Any]) -> str:
    """Render a dashboard widget using its configured template."""
    return render_template_string(widget_template, name=widget_name, **data)


def render_footer(footer_text: str) -> str:
    """Render a footer with user-provided text."""
    return render_template_string("<footer>{{ text }}</footer>", text=footer_text)


def render_admin_preview(html_fragment: str) -> str:
    """Render an admin-supplied HTML fragment inside a wrapper."""
    wrapper = f"<main>{html_fragment}</main>"
    return render_template_string(wrapper)


if __name__ == "__main__":
    print(render_footer("Quorum demo"))