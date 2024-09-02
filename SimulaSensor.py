import threading
import random
import time
from pymongo import MongoClient

# Configuração do MongoDB
client = MongoClient('localhost', 27017)
db = client.bancoiot
sensores_collection = db.sensores

# Inicializa os documentos para cada sensor
sensores = [
    {"nomeSensor": "Temp1", "valorSensor": 0, "unidadeMedida": "C°", "sensorAlarmado": False},
    {"nomeSensor": "Temp2", "valorSensor": 0, "unidadeMedida": "C°", "sensorAlarmado": False},
    {"nomeSensor": "Temp3", "valorSensor": 0, "unidadeMedida": "C°", "sensorAlarmado": False}
]

# Insere os documentos se eles ainda não existirem
for sensor in sensores:
    sensores_collection.update_one({"nomeSensor": sensor["nomeSensor"]}, {"$setOnInsert": sensor}, upsert=True)

def simula_sensor(nomeSensor):
    while True:
        sensor_doc = sensores_collection.find_one({"nomeSensor": nomeSensor})

        if sensor_doc["sensorAlarmado"]:
            print(f"Atenção! Temperatura muito alta! Verificar Sensor {nomeSensor}!")
            break

        temperatura = random.uniform(30, 40)
        print(f"Sensor {nomeSensor}: {temperatura:.2f} C°")

        # Atualiza o documento no MongoDB
        update_data = {"valorSensor": temperatura}

        if temperatura > 38:
            update_data["sensorAlarmado"] = True

        sensores_collection.update_one({"nomeSensor": nomeSensor}, {"$set": update_data})

        if update_data.get("sensorAlarmado"):
            print(f"Atenção! Temperatura muito alta! Verificar Sensor {nomeSensor}!")
            break

        time.sleep(5)  # Ajuste o tempo conforme necessário

# Criação das Threads
sensor1 = threading.Thread(target=simula_sensor, args=("Temp1",))
sensor2 = threading.Thread(target=simula_sensor, args=("Temp2",))
sensor3 = threading.Thread(target=simula_sensor, args=("Temp3",))

# Inicia as Threads
sensor1.start()
sensor2.start()
sensor3.start()

# Aguarda as Threads terminarem
sensor1.join()
sensor2.join()
sensor3.join()
