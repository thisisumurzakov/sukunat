from celery import shared_task

@shared_task
def send_distress_signal(contact_id):
    # Placeholder for sending SMS logic
    print(f"Simulated sending distress signal for contact ID: {contact_id}")
