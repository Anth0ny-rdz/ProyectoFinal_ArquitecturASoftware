import sqlite3

# Ruta al archivo de la base de datos SQLite
db_path = r'C:\Users\didie\Downloads\No se\ProyectoFinal_ArquitecturASoftware\P Final Arquitectura\reservations.sql'  # Reemplaza con la ruta a tu archivo de base de datos

# Nombre de la tabla a la que deseas agregar la columna
table_name = 'reservations'  # Reemplaza con el nombre de tu tabla

# Conectar a la base de datos
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Sentencia SQL para agregar la nueva columna "email"
alter_table_query = f'ALTER TABLE {table_name} ADD COLUMN email TEXT'

# Ejecutar la sentencia SQL
cursor.execute(alter_table_query)

# Confirmar los cambios
conn.commit()

# Cerrar la conexión
conn.close()

print("La nueva columna 'email' ha sido agregada con éxito.")
