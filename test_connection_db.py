import serial
from time import sleep
import db_connection as db
import requests

def read_card_uid():
    ser = serial.Serial('COM6', 9600, timeout=1)
    sleep(1)

    while True:
        card_uid = ser.readline().decode().strip('\n')   # read a byte
        if card_uid:

            db.cursor.execute(f'''
                SELECT id
                FROM patient_patient
                WHERE card_id = {card_uid}
            ''')
            ser.close()
            return db.cursor.fetchone()[0]


def add_visit(patient_id, medcin_id):

    r = requests.post("http://127.0.0.1:8000/doctor/create_visite", data={"patient": patient_id,
                                                               "medcin": medcin_id})

    print(r.status_code)



if __name__ == '__main__':
    add_visit(2, 123456)
    # print(read_card_uid())

