---
layout: page
title: People
permalink: /people/
---

<ul class="people-grid">
  {% assign sorted_people = site.people | sort: 'order' %}
  {% for person in sorted_people %}
  <li class="person-card">
    {% if person.photo and person.photo.size > 0 %}
    <img src="{{ person.photo | relative_url }}" alt="Photo of {{ person.title }}">
    {% endif %}
    <div class="person-card-body">
      <h3><a href="{{ person.url | relative_url }}">{{ person.title }}</a></h3>
      <p class="role">{{ person.role }}</p>
    </div>
  </li>
  {% endfor %}
</ul>

<!--
  TODO (Elyssa): add each lab member as a new file in the _people/
  folder — see SETUP.md for a copy-paste template. They'll show up here
  automatically, sorted by the `order` field in each file.
-->
