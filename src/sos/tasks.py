from celery import shared_task

@shared_task
def send_distress_signal(phone_number, latitude, longitude):

    # Format URLs for Google Maps and Yandex Maps
    google_maps_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
    yandex_maps_url = f"https://yandex.com/maps/?text={latitude},{longitude}"

    # Simulate sending an SMS
    message = f"Urgent: Your contact is in danger! Locate them here: Google Maps: {google_maps_url} or Yandex Maps: {yandex_maps_url}"
    print(message)  # This print statement is a placeholder for sending an SMS
