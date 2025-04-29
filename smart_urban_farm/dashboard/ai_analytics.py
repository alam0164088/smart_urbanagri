def predict_watering_schedule(sensor_data):
    latest = sensor_data[0]
    if latest.soil_moisture < 300:
        return "Water Now"
    return "No Water Needed"