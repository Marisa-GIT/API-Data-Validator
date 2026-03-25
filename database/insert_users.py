from api.external_api_testing.get_users import fetch_users
from database.db_connection import connect_db
from validation.validator import validate_user

# Cargar datos iniciales
def insert_users():

    users = fetch_users()

    conn = connect_db()
    cursor = conn.cursor()

    for user in users:

        is_valid = validate_user(user)

        query = """
        INSERT INTO users (id, name, email, username, valid)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            user["id"],
            user["name"],
            user["email"],
            user["username"],
            True if is_valid else False
        )

        cursor.execute(query, values)

    conn.commit()
    print("Usuarios insertados correctamente")

