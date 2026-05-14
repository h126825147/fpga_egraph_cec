def build_boolean_rules() -> list:
    """Return the first version of egglog rewrite rules."""
    return [
        # commutativity
        "(and ?a ?b) => (and ?b ?a)",
        "(or ?a ?b) => (or ?b ?a)",
        # associativity
        "(and (and ?a ?b) ?c) => (and ?a (and ?b ?c))",
        "(or (or ?a ?b) ?c) => (or ?a (or ?b ?c))",
        # distributivity
        "(and ?a (or ?b ?c)) => (or (and ?a ?b) (and ?a ?c))",
        "(or ?a (and ?b ?c)) => (and (or ?a ?b) (or ?a ?c))",
        # idempotency
        "(and ?a ?a) => (?a)",
        "(or ?a ?a) => (?a)",
    ]