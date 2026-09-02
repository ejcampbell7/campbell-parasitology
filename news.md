---
layout: page
title: News
permalink: /news/
---

<ul class="post-list">
  {% for post in site.posts %}
  <li>
    <span class="post-date">{{ post.date | date: "%b %-d, %Y" }}</span>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
  </li>
  {% endfor %}
</ul>

<!--
  TODO (Elyssa): add new posts as files in _posts/ named
  YYYY-MM-DD-short-title.md — see SETUP.md for a template. Newest posts
  appear at the top automatically.
-->
