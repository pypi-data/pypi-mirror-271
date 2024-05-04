from sqlglot import select, condition

where = condition("x=1").and_("y=1")
select("*").from_("y").join(where).sql()