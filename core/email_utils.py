from django.core.mail import send_mail
from django.conf import settings


def send_request_received_email(listing_owner, sender, listing):
    """Notify listing owner that a new roommate request was received."""
    subject = f'New Roommate Request — {listing.title}'
    message = f"""
Hi {listing_owner.first_name or listing_owner.username},

You have received a new roommate request for your listing:

Listing:  {listing.title}
Location: {listing.address}, {listing.city}
Rent:     €{listing.rent_per_month}/month

Request from: {sender.get_full_name() or sender.username}

Log in to NestMate to view and respond to this request:
http://127.0.0.1:8000/requests/

Regards,
NestMate Team
"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[listing_owner.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f'Email error (request received): {e}')


def send_request_accepted_email(req):
    """Notify sender that their roommate request was accepted."""
    subject = f'Your Roommate Request was Accepted — {req.listing.title}'
    message = f"""
Hi {req.sender.first_name or req.sender.username},

Great news! Your roommate request has been accepted.

Listing:  {req.listing.title}
Location: {req.listing.address}, {req.listing.city}
Rent:     €{req.listing.rent_per_month}/month
Owner:    {req.listing.owner.get_full_name() or req.listing.owner.username}
Email:    {req.listing.owner.email}

Please contact the listing owner directly to arrange next steps.

Log in to NestMate to view your requests:
http://127.0.0.1:8000/requests/

Regards,
NestMate Team
"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[req.sender.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f'Email error (request accepted): {e}')


def send_request_rejected_email(req):
    """Notify sender that their roommate request was rejected."""
    subject = f'Update on Your Roommate Request — {req.listing.title}'
    message = f"""
Hi {req.sender.first_name or req.sender.username},

Thank you for your interest. Unfortunately your roommate request for the following listing was not successful this time:

Listing:  {req.listing.title}
Location: {req.listing.address}, {req.listing.city}
Rent:     €{req.listing.rent_per_month}/month

Please continue browsing other available listings on NestMate:
http://127.0.0.1:8000/listings/

Regards,
NestMate Team
"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[req.sender.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f'Email error (request rejected): {e}')
