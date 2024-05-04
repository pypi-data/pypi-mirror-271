from sqlglot import parse, condition


def _generate_join_clause(joins):
    clauses = []
    if len(joins) > 0:
        for join in joins:
            join_table = join["name"]
            join_alias = join["alias"]
            join_conditions = " AND ".join([
                f"{cond['left']['alias']}.{cond['left']['name']} = {cond['right']['alias']}.{cond['right']['name']}"
                for cond in join["on"]
            ])
            clause = f"JOIN {join_table} AS {join_alias} ON {join_conditions}"
            clauses.append(clause)
    else:
        return ""
    return " ".join(clauses)


def _generate_expr(expr):
    if "expr" in expr:
        data_expr = expr["expr"]
        if "column" in data_expr:
            column = f"{data_expr['column']['alias']}.{data_expr['column']['name']}"
            operator = data_expr["operator"]
            value = data_expr["value"][0]
            return f"{column} {operator} '{value}'"
        elif "booleanOperator" in data_expr:
            return data_expr["booleanOperator"]
    elif "booleanOperator" in expr:
        return expr["booleanOperator"]


def _generate_order_by_clause(order_by):
    clauses = [f"{item['column']['alias']}.{item['column']['name']} {item.get('order', 'ASC')}" for item in order_by]
    return "ORDER BY " + ", ".join(clauses) if clauses else ""


def _generate_where_clause(conditions):
    where_conditions = []
    for cond_metadata in conditions:
        if "listOfExpr" in cond_metadata:
            sublist = [_generate_expr(expr) for expr in cond_metadata["listOfExpr"]]
            where_conditions.append(" ".join(sublist))
        elif "expr" in cond_metadata and "column" in cond_metadata["expr"]:
            # expr = cond_metadata["expr"]
            where_conditions.append(_generate_expr(cond_metadata))
    where_condition = " AND ".join(where_conditions)
    return f"WHERE {where_condition}" if where_condition else ""


def generate_data_query(json_data):
    queries = []
    for entity in json_data:
        select_clause = ", ".join([f"{item['name']}" for item in entity["select"]])
        from_table = entity["fromTable"]["name"]
        table_alias = entity["fromTable"]["alias"]
        join_clause = _generate_join_clause(entity.get("join", []))
        where_clause = _generate_where_clause(entity.get("where", []))
        order_by_clause = _generate_order_by_clause(entity.get("order_by", []))

        sql_query = f"SELECT {select_clause} FROM {from_table} {table_alias} {join_clause} {where_clause} {order_by_clause}"

        # parsed_query = parse(sql_query)
        queries.append({"tableName": from_table, "query": str(sql_query)})
    return queries
