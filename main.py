from api.external_api_testing.get_users import fetch_users
from validation.validator import validate_user
from database.db_connection import connect_db
from api.api_tests import test_get_users

def main():
    # Contadores de resultados
    pass_count = 0
    fail_count = 0

    # Obtener usuarios
    users = fetch_users()

    if not users:
        print("⚠️ No se obtuvieron usuarios desde la API")
        return

    # Conectar a la base de datos
    try:
        conn = connect_db()
        cursor = conn.cursor()
    except Exception as e:
        print(f"❌ Error conectando a la DB: {e}")
        return

    # Query SQL
    query = """
    INSERT INTO test_results (user_id, test_name, result, message)
    VALUES (%s, %s, %s, %s)
    """

    records = []

    # =========================
    # 🌐 TESTS DE API
    # =========================
    api_results = test_get_users()

    print("\n🌐 TESTS DE API")

    for test_name, result, message in api_results:
        print(test_name, result, message)

        if result == "PASS":
            pass_count += 1
        else:
            fail_count += 1

        # Guardar también tests de API
        records.append((None, test_name, result, message))

    # =========================
    # 👤 VALIDACIÓN DE USUARIOS
    # =========================
    for user in users:
        user_id = user.get("id")

        if not user_id:
            print("⚠️ Usuario sin ID:", user)
            continue

        test_results = validate_user(user)

        for test_name, result, message in test_results:

            if result == "PASS":
                pass_count += 1
            else:
                fail_count += 1

            records.append((user_id, test_name, result, message))

    # =========================
    # 💾 GUARDAR EN DB
    # =========================
    try:
        cursor.executemany(query, records)
        conn.commit()
    except Exception as e:
        print(f"❌ Error insertando datos: {e}")
    finally:
        cursor.close()
        conn.close()

    # =========================
    # 📊 REPORTE FINAL
    # =========================
    total = pass_count + fail_count

    print("\n📊 REPORTE DE PRUEBAS")
    print(f"PASS: {pass_count}")
    print(f"FAIL: {fail_count}")

    if total > 0:
        success_rate = (pass_count / total) * 100
        print(f"📈 Éxito: {success_rate:.2f}%")

    print("\n✅ Datos guardados correctamente")


# Ejecutar script
if __name__ == "__main__":
    main()