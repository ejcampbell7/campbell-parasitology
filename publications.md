---
layout: page
title: Publications
permalink: /publications/
---

<p>
  This list syncs automatically from
  <a href="https://orcid.org/{{ site.orcid }}" target="_blank" rel="noopener">my ORCID record</a>.
</p>

<ul class="pub-list">
  {% assign sorted_pubs = site.publications | sort: 'year' | reverse %}
  {% for pub in sorted_pubs %}
  <li>
    <div class="pub-title">
      {% if pub.external_url %}
      <a href="{{ pub.external_url }}" target="_blank" rel="noopener">{{ pub.title }}</a>
      {% else %}
      {{ pub.title }}
      {% endif %}
    </div>
    <div class="pub-meta">
      {%- capture meta -%}
        {%- if pub.authors -%}{{ pub.authors }}{%- endif -%}
        {%- if pub.citation -%}{% if pub.authors %} &middot; {% endif %}{{ pub.citation }}{%- endif -%}
        {%- if pub.doi -%}{% if pub.authors or pub.citation %} &middot; {% endif %}DOI: {{ pub.doi }}{%- endif -%}
      {%- endcapture -%}
      {{ meta }}
    </div>
  </li>
  {% endfor %}
</ul>

<!--
  Publications prefixed "orcid-" in _publications/ are generated
  automatically by scripts/sync_orcid_publications.py (see SETUP.md,
  "Set up automatic ORCID sync") — don't hand-edit those, they'll be
  overwritten on the next sync. To add something ORCID doesn't have
  (e.g. a preprint), add a normally-named file instead — see SETUP.md.
-->
