import serial
from time import sleep
import db_connection as db
import datetime


def read_card_uid():
    ser = serial.Serial('COM6', 9600, timeout=1)
    sleep(1)

    while True:
        card_uid = ser.readline().decode().strip('\n')   # read a byte
        if card_uid:
            # timestamp = datetime.datetime.now()
            # date = timestamp.strftime("%m-%d-%Y")
            # time = timestamp.strftime("%H:%M:%S")
            # print(card_uid)

            db.cursor.execute(f'''
                SELECT * 
                FROM {db.db_name}.users
                WHERE card_id = {card_uid}
            ''')

            ser.close()
            return db.cursor.fetchone()

if __name__ == '__main__':
    print(read_card_uid())