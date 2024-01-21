{% macro percent_profit(column_name1, column_name2) %}
    (({{ column_name1 }} - {{column_name2 }}) / {{ column_name2 }} * 100)
{% endmacro %}