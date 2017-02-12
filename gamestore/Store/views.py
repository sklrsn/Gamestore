from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import cloudinary
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from Users.models import UserProfile
from GameArena.models import Game
from .models import Purchase, Cart, Order
from .forms import CartForm
from django.db.models import Sum, F
from hashlib import md5
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
# Secret key details from payment gateway -
#   Selled ID: kalairajsunil
#   Secret Key: 3d5e7a6cfcaf44600e6a2650326780c2


def home(request):
    return render(request=request, template_name='store.html')


"""
TODO: Add proper comments
View for game store
"""
@login_required
def index(request):
    user = User.objects.get(username=request.user)
    current_user = UserProfile.objects.get(user=user)
    games_list = Game.objects.all()
    purchse_list = Purchase.objects.filter(player_details=user)
    onlypurchase = Game.objects.exclude(id__in=purchse_list.values('game_details'))
    return render(request, 'store.html',
                  {'games_list': games_list})

@login_required
def add_to_cart(request):
    user = User.objects.get(username=request.user)
    current_user = UserProfile.objects.get(user=user)
    form = CartForm(request.POST)
    jsondata={}
    if not form.is_valid():
        jsondata['error'] = form.errors
        return JsonResponse(status=400, data=jsondata)
    if form.cleaned_data['action'] == 'add':
        # TODO: Check for owned games
        # TODO: Check if already in cart

        cart = Cart(id=None,player_details=user,game_details=form.cleaned_data['game'])
        cart.save()

    return JsonResponse(status=201, data=jsondata)

@login_required
def remove_from_cart(request):
    user = User.objects.get(username=request.user)
    current_user = UserProfile.objects.get(user=user)
    form = CartForm(request.POST)
    jsondata={}
    if not form.is_valid():
        jsondata['error'] = form.errors
        return JsonResponse(status=400, data=jsondata)
    if form.cleaned_data['action'] == 'remove':
        # TODO: Check for owned games
        # TODO: Check if already in cart
        cart = Cart.objects.filter(player_details = user, game_details = form.cleaned_data['game'])
        if cart:
            cart.delete()
        else:
            jsondata['error'] = "Game not in cart"
            return JsonResponse(status=401, data=jsondata)

    return JsonResponse(status=201, data=jsondata)
@login_required
def get_cart(request):
    user = User.objects.get(username=request.user)
    current_user = UserProfile.objects.get(user=user)
    cartitems = Cart.objects.filter(player_details=user)
    paginator = Paginator(cartitems, 1)
    page = request.GET.get('page', 1)

    try:
        carts = paginator.page(page)
    except PageNotAnInteger:
        carts = paginator.page(1)
    except EmptyPage:
        carts = paginator.page(paginator.num_pages)
    '''
        Write the code to return the cart details
    '''
    return render(request, 'cart.html',
                  {'cart_list': carts})

@login_required
def purchase(request):
    user = User.objects.get(username=request.user)
    current_user = UserProfile.objects.get(user=user)
    #amount =Cart.objects.annotate(Sum(F('game_details__cost')))

    order = Order(id=None)
    order.save()
    print('Order : ' + str(order.id))
    Cart.objects.filter(player_details=user).update(order=order)
    cartitems = Cart.objects.filter(player_details=user)
    amount=cartitems.aggregate(Sum('game_details__cost'))['game_details__cost__sum']
    print("amount:"+str(amount))
    # payment gateway Configuration

    action = "http://payments.webcourse.niksula.hut.fi/pay/"
    pid = order.id
    print("pid"+str(pid))
    sid = "kalairajsunil"  # Fixme Todo: parametrize
    success_url = request.build_absolute_uri(reverse("payment_success"))
    cancel_url = request.build_absolute_uri(reverse("payment_cancel"))
    error_url = request.build_absolute_uri(reverse("payment_failure"))
    secret_key = "3d5e7a6cfcaf44600e6a2650326780c2"  # Fixme Todo: parametrize
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)  # Fixme Todo: parametrize, secret key!
    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()
    return render(request, 'purchase.html',
                  {'cart_list': cartitems,
                  'action': action,
                   'pid': pid,
                   'sid': sid,
                   'amount': amount,
                   'success_url': success_url,
                   'cancel_url': cancel_url,
                   'error_url': error_url,
                   'checksum': checksum})

@login_required
def purchase_response(request):
    pid = request.GET['pid']
    ref = request.GET['ref']
    result = request.GET['result']
    checksum = request.GET['checksum']
    response = pid + " : " +ref  + " : " +result + " : " +checksum
    order = Order.objects.get(id=pid)
    order.paymentRef = ref
    order.checksum = checksum
    order.status = result
    order.save()
    if(result=="success"):
        Cart.objects.filter(order=order).delete()
    return HttpResponse(response)
