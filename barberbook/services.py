def active_services(services):
    return [service for service in services if service.active]

def validate_service(service):
    if not service.active or service.minutes <= 0 or service.price < 0:
        raise ValueError('Invalid or inactive service')
