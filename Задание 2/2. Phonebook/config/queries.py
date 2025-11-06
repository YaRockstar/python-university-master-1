CREATE_CONTACTS_TABLE = """
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT
            )
            """

INSERT_INTO_CONTACTS = "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)"

SELECT_CONTACTS = "SELECT id, name, phone, email FROM contacts ORDER BY id"

SELECT_CONTACT_BY_ID = "SELECT id, name, phone, email FROM contacts WHERE id = ?"

SELECT_CONTACT_BY_NAME_AND_PHONE = "SELECT id FROM contacts WHERE name = ? AND phone = ?"

UPDATE_CONTACT = "UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?"

DELETE_CONTACT_BY_ID = "DELETE FROM contacts WHERE id = ?"
