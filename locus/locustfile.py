from locust import HttpUser, task, between

class UsuarioDeCarga(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def hacer_inferencia(self):
        payload = {
            "bill_depth_mm": 18.7,
            "bill_length_mm": 39.1,
            "body_mass_g": 3750,
            "flipper_length_mm": 181,
            "island": 0,
            "sex": 1,
            "year": 2007
        }
        # Enviar una petición POST al endpoint /predict
        response = self.client.post("/predict", json=payload)
        # Opcional: validación de respuesta
        if response.status_code != 200:
            print("❌ Error en la inferencia:", response.text)