from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .models import StudentProfile, Listing, RoommateRequest
from .forms import RegisterForm, StudentProfileForm, ListingForm, RoommateRequestForm
from .email_utils import (
    send_request_received_email,
    send_request_accepted_email,
    send_request_rejected_email,
)


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user, college='')
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome aboard.')
            return redirect('profile_edit')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})


@login_required
def dashboard(request):
    listings = Listing.objects.filter(status='available').order_by('-created_at')[:6]
    my_listings = Listing.objects.filter(owner=request.user).count()
    my_requests = RoommateRequest.objects.filter(sender=request.user).count()
    pending_requests = RoommateRequest.objects.filter(
        listing__owner=request.user, status='pending'
    ).count()
    total_listings = Listing.objects.filter(status='available').count()
    context = {
        'listings': listings,
        'my_listings': my_listings,
        'my_requests': my_requests,
        'pending_requests': pending_requests,
        'total_listings': total_listings,
    }
    return render(request, 'core/dashboard.html', context)


# --- LISTINGS CRUD ---

@login_required
def listing_list(request):
    query = request.GET.get('q', '')
    city = request.GET.get('city', '')
    property_type = request.GET.get('property_type', '')
    max_rent = request.GET.get('max_rent', '')
    listings = Listing.objects.filter(status='available')
    if query:
        listings = listings.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(address__icontains=query)
        )
    if city:
        listings = listings.filter(city__icontains=city)
    if property_type:
        listings = listings.filter(property_type=property_type)
    if max_rent:
        try:
            listings = listings.filter(rent_per_month__lte=float(max_rent))
        except ValueError:
            pass
    context = {
        'listings': listings,
        'query': query,
        'city': city,
        'property_type': property_type,
        'max_rent': max_rent,
        'property_types': Listing.PROPERTY_TYPES,
    }
    return render(request, 'core/listing_list.html', context)


@login_required
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    existing_request = None
    if request.user != listing.owner:
        existing_request = RoommateRequest.objects.filter(
            listing=listing, sender=request.user
        ).first()
    requests = RoommateRequest.objects.filter(listing=listing) if request.user == listing.owner else None
    return render(request, 'core/listing_detail.html', {
        'listing': listing,
        'existing_request': existing_request,
        'requests': requests,
    })


@login_required
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            messages.success(request, 'Listing created successfully!')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, 'core/listing_form.html', {'form': form, 'action': 'Create'})


@login_required
def listing_edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Listing updated successfully!')
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
    return render(request, 'core/listing_form.html', {'form': form, 'action': 'Edit', 'listing': listing})


@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing deleted successfully.')
        return redirect('my_listings')
    return render(request, 'core/listing_confirm_delete.html', {'listing': listing})


@login_required
def my_listings(request):
    listings = Listing.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'core/my_listings.html', {'listings': listings})


# --- ROOMMATE REQUESTS CRUD ---

@login_required
def request_create(request, listing_pk):
    listing = get_object_or_404(Listing, pk=listing_pk)
    if listing.owner == request.user:
        messages.error(request, "You cannot request your own listing.")
        return redirect('listing_detail', pk=listing_pk)
    if RoommateRequest.objects.filter(listing=listing, sender=request.user).exists():
        messages.warning(request, "You have already sent a request for this listing.")
        return redirect('listing_detail', pk=listing_pk)
    if request.method == 'POST':
        form = RoommateRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.listing = listing
            req.sender = request.user
            req.save()
            send_request_received_email(listing.owner, request.user, listing)
            messages.success(request, 'Request sent successfully! The owner has been notified by email.')
            return redirect('my_requests')
    else:
        form = RoommateRequestForm()
    return render(request, 'core/request_form.html', {'form': form, 'listing': listing})


@login_required
def my_requests(request):
    sent = RoommateRequest.objects.filter(sender=request.user).order_by('-created_at')
    received = RoommateRequest.objects.filter(listing__owner=request.user).order_by('-created_at')
    return render(request, 'core/my_requests.html', {'sent': sent, 'received': received})


@login_required
def request_update_status(request, pk):
    req = get_object_or_404(RoommateRequest, pk=pk, listing__owner=request.user)
    if request.method == 'POST':
        status = request.POST.get('status')

        if status == 'accepted':
            req.status = 'accepted'
            req.save()
            # Auto-change listing to Taken
            req.listing.status = 'taken'
            req.listing.save()
            # Auto-reject all other pending requests for same listing
            RoommateRequest.objects.filter(
                listing=req.listing, status='pending'
            ).exclude(pk=req.pk).update(status='rejected')
            # Send acceptance email
            send_request_accepted_email(req)
            messages.success(request, f'Request accepted. {req.sender.get_full_name() or req.sender.username} has been notified by email. Listing marked as Taken.')

        elif status == 'rejected':
            req.status = 'rejected'
            req.save()
            # Send rejection email
            send_request_rejected_email(req)
            messages.success(request, 'Request rejected. The applicant has been notified by email.')

    return redirect('my_requests')


@login_required
def request_withdraw(request, pk):
    req = get_object_or_404(RoommateRequest, pk=pk, sender=request.user)
    if request.method == 'POST':
        req.status = 'withdrawn'
        req.save()
        messages.success(request, 'Request withdrawn.')
    return redirect('my_requests')


# --- PROFILE CRUD ---

@login_required
def profile_view(request, pk=None):
    if pk:
        user_profile = get_object_or_404(StudentProfile, user__pk=pk)
    else:
        user_profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    return render(request, 'core/profile.html', {'profile': user_profile})


@login_required
def profile_edit(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_view')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'core/profile_form.html', {'form': form})
