import mysql.connector
import spms_cloud_control
from time import sleep
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "plantenna",
    database = "plantenna"
    )
mycursor = mydb.cursor()
def insert_data(temp, humidity, batV, airflow, pressure):
    sql = "INSERT INTO Sensor_data(temperature, humidity, battery_voltage, airflow, pressure) " \
            "VALUES(%s,%s,%s,%s,%s)"
    val = (temp, humidity, batV, airflow, pressure)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
          
def return_data():
    mycursor.execute ("SELECT * FROM Sensor_data")
    myresult = mycursor.fetchall()
    return(myresult)
##        for result in myresult:
##            date = str(result[6].date())
##            time = str(result[6].time())
##            temperature = float(result[1])/100
##            humidity = float(result[2])/100
##            batV = float(result[3])*20
##            airflow = float(result[4])
##            pressure = float(result[5])
##            print(result)
##            spms_mqtt_client = spms_cloud_control.spms_mqtt_init()
##            while(1):
##                if (spms_mqtt_client != False):
##                    try:
##                        spms_cloud_control.spms_mqtt_send_data(spms_mqtt_client, temperature, humidity, pressure, batV, airflow, date, time)
##                        sleep(1)
##                    except:
##                        break
##                else:
##                    break
                    
                
def remove_data(num):
    sql = "DELETE FROM Sensor_data WHERE number = " + str(num)
    mycursor.execute(sql)
    mydb.commit()
    #print('1 row removed from DB')


def main():
    print('a')
##    for i in range(10):
##        insert_data('23','90','10','12','3')
##    return_data()
##    remove_data(1120)
if __name__ == '__main__':
    main()
    
