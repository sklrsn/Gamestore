from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from Users.models import UserProfile
from GameArena.models import Game, Category
from .models import Purchase, Cart, Order
from .forms import CartForm
from django.db.models import Sum
from hashlib import md5
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

"""
@Method_Name: index
@Param_in: request
@:returns: renders the store page
"""


@login_required
def index(request):
    concept = request.GET.get('concept', "")
    param = request.GET.get('param', "")
    print(concept)
    print(param)
    if concept == "All":
        concept = ""

    if concept != "":
        games_list = Game.objects.filter(
            game_category=Category.objects.get(name=concept),
            description__contains=param)
    else:
        games_list = Game.objects.filter(
            description__contains=param)
    page_size = getattr(settings, "PAGE_SIZE", 1)
    print(page_size[0])
    paginator = Paginator(games_list, int(page_size[0]))
    page = request.GET.get('page', int(page_size[0]))
    try:
        games = paginator.page(page)
    except PageNotAnInteger:
        games = paginator.page(int(page_size[0]))
    except EmptyPage:
        games = paginator.page(paginator.num_pages)

    games_category = Category.objects.all()
    return render(request, 'store/store.html',
                  {'games_list': games,
                   'user_type': request.user.userprofile.user_type, 'games_category': games_category})


"""
@Method_Name: add_to_cart
@Param_in: request
@:returns: returns a JSON response
"""


@login_required
def add_to_cart(request):
    try:
        user = User.objects.get(username=request.user)
        form = CartForm(request.POST)
        jsondata = {}
        if not form.is_valid():
            jsondata['error'] = form.errors
            return JsonResponse(status=400, data=jsondata)
        if form.cleaned_data['action'] == 'add':
            # TODO: Check for owned games
            game = form.cleaned_data['game']
            '''
                Check for owned games
            '''
            ownedGames = Purchase.objects.filter(game_details=game, player_details=user)
            if ownedGames.count() > 0:
                return JsonResponse(status=402, data=jsondata)
            '''
                Check for games already added in cart
            '''
            cartitems = Cart.objects.filter(player_details=user, game_details=game)
            if cartitems.count() > 0:
                return JsonResponse(status=403, data=jsondata)
            '''
                Add the game to cart
            '''
            cart = Cart(id=None, player_details=user, game_details=game)
            cart.save()

        return JsonResponse(status=201, data=jsondata)
    except:
        return JsonResponse(status=400, data=jsondata)


"""
@Method_Name: remove_from_cart
@Param_in: request
@:returns: JSON response
"""


@login_required
def remove_from_cart(request):
    user = User.objects.get(username=request.user)
    form = CartForm(request.POST)
    jsondata = {}
    if not form.is_valid():
        jsondata['error'] = form.errors
        return JsonResponse(status=400, data=jsondata)
    if form.cleaned_data['action'] == 'remove':
        # TODO: Check for owned games
        # TODO: Check if already in cart
        cart = Cart.objects.filter(player_details=user, game_details=form.cleaned_data['game'])
        if cart:
            cart.delete()
        else:
            jsondata['error'] = "Game not in cart"
            return JsonResponse(status=401, data=jsondata)

    return JsonResponse(status=201, data=jsondata)


"""
@Method_Name: get_cart
@Param_in: request
@:returns: renders cart page
"""


@login_required
def get_cart(request):
    page_size = getattr(settings, "PAGE_SIZE", 5)
    user = User.objects.get(username=request.user)
    cartitems = Cart.objects.filter(player_details=user)
    paginator = Paginator(cartitems, int(page_size[0]))
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
    return render(request, 'store/cart.html',
                  {'cart_list': carts,
                   'user_type': request.user.userprofile.user_type})


"""
@Method_Name: purchase
@Param_in: request
@:returns: renders the success of the purchase
"""


@login_required
def purchase(request):
    user = User.objects.get(username=request.user)
    current_user = UserProfile.objects.get(user=user)

    cartitems = Cart.objects.filter(player_details=user)
    order = Order(id=None)
    order.save()
    cartitems.update(order=order)
    amount = cartitems.aggregate(Sum('game_details__cost'))['game_details__cost__sum']

    action = "http://payments.webcourse.niksula.hut.fi/pay/"
    pid = order.id

    sid = "kalairajsunil"
    secret_key = "3d5e7a6cfcaf44600e6a2650326780c2"

    success_url = request.build_absolute_uri(reverse("payment_response"))
    cancel_url = request.build_absolute_uri(reverse("purchase"))
    error_url = request.build_absolute_uri(reverse("payment_failure"))
    checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount,
                                                            secret_key)

    m = md5(checksumstr.encode("ascii"))
    checksum = m.hexdigest()

    return render(request, 'store/purchase.html',
                  {'cart_list': cartitems,
                   'user_type': current_user.user_type,
                   'action': action,
                   'pid': pid,
                   'sid': sid,
                   'amount': amount,
                   'success_url': success_url,
                   'cancel_url': cancel_url,
                   'error_url': error_url,
                   'checksum': checksum})


"""
@Method_Name: purhcase_response
@Param_in: request
@:returns: HTTP response
"""


@login_required
def purchase_response(request):
    pid = request.GET['pid']
    ref = request.GET['ref']
    result = request.GET['result']
    checksum = request.GET['checksum']
    sid = "kalairajsunil"
    secret_key = "3d5e7a6cfcaf44600e6a2650326780c2"

    response = pid + " : " + ref + " : " + result + " : " + checksum
    order = Order.objects.get(id=pid)

    cartitems = order.order_cartitems.all()

    checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)
    m = md5(checksumstr.encode("ascii"))
    checksum_check = m.hexdigest()

    if checksum_check != checksum:
        return HttpResponseRedirect(redirect_to=reverse("payment_failure"))
    order.paymentRef = ref
    order.checksum = checksum
    order.status = result
    order.save()
    if result == "success":
        for item in cartitems:
            purchase = Purchase(game_details=item.game_details, player_details=item.player_details,
                                cost=item.game_details.cost, order=order)
            purchase.save()
            item.delete()
    return HttpResponseRedirect(redirect_to=reverse("payment_success"))


def payment_failure(request):
    return render(request, 'store/payment_error.html')


def payment_success(request):
    return render(request, 'store/payment_successful.html', {'username': request.user.username})
