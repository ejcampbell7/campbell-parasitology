---
layout: page
title: People
permalink: /people/
---

<div class="people-group-photo">
  <img src="{{ '/assets/images/people/lab-group.jpg' | relative_url }}" alt="The Campbell Parasitology Lab">
</div>

<ul class="people-list">
  {% assign sorted_people = site.people | sort: 'order' %}
  {% for person in sorted_people %}
  <li class="person-entry">
    <div class="person-entry-header">
      {% if person.photo and person.photo.size > 0 %}
      <img src="{{ person.photo | relative_url }}" alt="Photo of {{ person.title }}" class="person-entry-photo">
      {% endif %}
      <div>
        <h3>{{ person.title }}</h3>
        {% if person.role %}<p class="role">{{ person.role }}</p>{% endif %}
        {% if person.orcid %}<p class="orcid"><a href="https://orcid.org/{{ person.orcid }}" target="_blank" rel="noopener">ORCID: {{ person.orcid }}</a></p>{% endif %}
      </div>
    </div>
    {% if person.content and person.content.size > 0 %}
    <div class="person-entry-bio">
      {{ person.content }}
    </div>
    {% endif %}
  </li>
  {% endfor %}
</ul>
