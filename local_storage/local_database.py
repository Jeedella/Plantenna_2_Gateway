from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config

def insert_data(temp, humidity, batV, airflow, pressure):
    query = "INSERT INTO Sensor_data(temperature, humidity, battery_voltage, airflow, pressure) " \
            "VALUES(%s,%s,%s,%s,%s)"
    args = (temp, humidity, batV, airflow, pressure)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

def main():
    for i in range(10):
        insert_data('23','90','10','12','3')

if __name__ == '__main__':
    main()
