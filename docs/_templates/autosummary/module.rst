{% block title -%}

{%- if fullname.startswith("openff") and fullname.count(".") == 1 -%}
{%- set title = fullname -%}
{%- else -%}
{%- set title = objname -%}
{%- endif -%}
{{ ("``" ~ title ~ "``") | underline('=')}}

{%- endblock %}
{% block base %}

.. automodule:: {{ fullname }}

   {% block modules %}
   {% if modules %}
   .. rubric:: Modules

   .. autosummary::
      :caption: Modules
      :toctree:
      :recursive:
   {% for item in modules %}
   {%- if item not in exclude_modules %}
      ~{{ item }}
   {% endif -%}
   {%- endfor %}

   {% endif %}
   {% endblock %}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: {{ _('Module Attributes') }}

   .. autosummary::
      :caption: Attributes
      :toctree:
      :nosignatures:
   {% for item in attributes %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {%- endblock -%}

   {% block functions %}
   {% if functions %}
   .. rubric:: {{ _('Functions') }}

   .. autosummary::
      :caption: Functions
      :toctree:
      :nosignatures:
   {% for item in functions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block classes %}

   {%- set types = [] -%}
   {%- for item in members -%}
      {%- if not item.startswith('_') and not (
         item in functions
         or item in attributes
         or item in exceptions
         or fullname ~ "." ~ item in modules
         or item in methods
      ) -%}
         {%- set _ = types.append(item) -%}
      {%- endif -%}
   {%- endfor %}

   {% if types %}
   .. rubric:: {{ _('Classes') }}

   .. autosummary::
      :caption: Classes
      :toctree:
      :nosignatures:
   {% for item in types %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block exceptions %}
   {% if exceptions %}
   .. rubric:: {{ _('Exceptions') }}

   .. autosummary::
      :caption: Exceptions
      :toctree:
      :nosignatures:
   {% for item in exceptions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

{% endblock %}
