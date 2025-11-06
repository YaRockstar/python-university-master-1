CREATE_EXPENSE_TABLE = """
    CREATE TABLE IF NOT EXISTS expense (
        expense_id INTEGER PRIMARY KEY
    );
"""

CREATE_EXPENSE_AMOUNT_TABLE = """
    CREATE TABLE IF NOT EXISTS expense_amount (
        expense_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        valid_from TEXT NOT NULL,
        FOREIGN KEY (expense_id) REFERENCES expense(expense_id)
    );
"""

CREATE_EXPENSE_DATE_TABLE = """
    CREATE TABLE IF NOT EXISTS expense_date (
        expense_id INTEGER NOT NULL,
        date_value TEXT NOT NULL CHECK(date_value GLOB '????-??-??'),
        valid_from TEXT NOT NULL,
        FOREIGN KEY (expense_id) REFERENCES expense(expense_id)
    );
"""

CREATE_EXPENSE_DESCRIPTION_TABLE = """
    CREATE TABLE IF NOT EXISTS expense_description (
        expense_id INTEGER NOT NULL,
        description TEXT,
        valid_from TEXT NOT NULL,
        FOREIGN KEY (expense_id) REFERENCES expense(expense_id)
    );
"""

CREATE_CATEGORY_KNOT_TABLE = """
    CREATE TABLE IF NOT EXISTS category_knot (
        category_id INTEGER PRIMARY KEY,
        category_name TEXT UNIQUE NOT NULL
    );
"""

CREATE_EXPENSE_CATEGORY_TABLE = """
    CREATE TABLE IF NOT EXISTS expense_category (
        expense_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        valid_from TEXT NOT NULL,
        FOREIGN KEY (expense_id) REFERENCES expense(expense_id),
        FOREIGN KEY (category_id) REFERENCES category_knot(category_id),
        UNIQUE (expense_id, category_id, valid_from)
    );
"""

INSERT_INTO_EXPENSE = """
    INSERT INTO expense DEFAULT VALUES;
"""

INSERT_INTO_EXPENSE_AMOUNT = """
    INSERT INTO expense_amount (expense_id, amount, valid_from) VALUES (?, ?, ?);
"""

INSERT_INTO_EXPENSE_DATE = """
    INSERT INTO expense_date (expense_id, date_value, valid_from) VALUES (?, ?, ?);
"""

INSERT_INTO_EXPENSE_DESCRIPTION = """
    INSERT INTO expense_description (expense_id, description, valid_from) VALUES (?, ?, ?);
"""

INSERT_INTO_CATEGORY_KNOT = """
    INSERT OR IGNORE INTO category_knot (category_name) VALUES (?);
"""

INSERT_INTO_EXPENSE_CATEGORY = """
    INSERT INTO expense_category (expense_id, category_id, valid_from) VALUES (?, ?, ?);
"""

SELECT_ALL_EXPENSES = """
    SELECT
        e.expense_id,
        a.amount,
        d.date_value AS date,
        c.category_name AS category,
        ed.description
    FROM expense e
    LEFT JOIN expense_amount a ON e.expense_id = a.expense_id
    LEFT JOIN expense_date d ON e.expense_id = d.expense_id
    LEFT JOIN expense_description ed ON e.expense_id = ed.expense_id
    LEFT JOIN expense_category ec ON e.expense_id = ec.expense_id
    LEFT JOIN category_knot c ON ec.category_id = c.category_id
    ORDER BY d.date_value DESC, e.expense_id DESC;
"""

SELECT_EXPENSE_BY_ID = """
    SELECT
        e.expense_id,
        a.amount,
        d.date_value AS date,
        c.category_name AS category,
        ed.description
    FROM expense e
    LEFT JOIN expense_amount a ON e.expense_id = a.expense_id
    LEFT JOIN expense_date d ON e.expense_id = d.expense_id
    LEFT JOIN expense_description ed ON e.expense_id = ed.expense_id
    LEFT JOIN expense_category ec ON e.expense_id = ec.expense_id
    LEFT JOIN category_knot c ON ec.category_id = c.category_id
    WHERE e.expense_id = ?;
"""

SELECT_EXPENSE_BY_CATEGORY = """
    SELECT
        e.expense_id,
        a.amount,
        d.date_value AS date,
        c.category_name AS category,
        ed.description
    FROM expense e
    LEFT JOIN expense_amount a ON e.expense_id = a.expense_id
    LEFT JOIN expense_date d ON e.expense_id = d.expense_id
    LEFT JOIN expense_description ed ON e.expense_id = ed.expense_id
    LEFT JOIN expense_category ec ON e.expense_id = ec.expense_id
    LEFT JOIN category_knot c ON ec.category_id = c.category_id
    WHERE c.category_name = ?
    ORDER BY d.date_value DESC, e.expense_id DESC;
"""

SELECT_EXPENSE_BY_DATE = """
    SELECT
        e.expense_id,
        a.amount,
        d.date_value AS date,
        c.category_name AS category,
        ed.description
    FROM expense e
    LEFT JOIN expense_amount a ON e.expense_id = a.expense_id
    LEFT JOIN expense_date d ON e.expense_id = d.expense_id
    LEFT JOIN expense_description ed ON e.expense_id = ed.expense_id
    LEFT JOIN expense_category ec ON e.expense_id = ec.expense_id
    LEFT JOIN category_knot c ON ec.category_id = c.category_id
    WHERE d.date_value = ?
    ORDER BY e.expense_id DESC;
"""

SELECT_CATEGORY_BY_NAME = """
    SELECT category_id, category_name
    FROM category_knot
    WHERE category_name = ?;
"""
