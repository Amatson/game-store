import json
from hashlib import md5

from django.conf import settings
from django.contrib.auth import authenticate, logout, update_session_auth_hash
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.defaults import permission_denied, bad_request

from gamestore.exceptions import BadRequest
from gamestore.forms import LoginForm, GameForm, RegisterForm, ScoreForm, SaveForm, EditNameForm, EditPasswordForm, \
    RequestLoadForm, EditGameForm, SearchForm
from .models import Player, Developer, Game, HighScore, Order, SaveState


def gameplay(request, gameid):
    """Gameplay view for individual games. Handles messages from game to service and service to game."""
    # The game in the iframe
    game = Game.objects.get(pk=gameid)

    # Check if the player has bought the game and can play it
    if hasattr(request.user, 'player'):
        player_owns_game = request.user.player.owned_games.filter(pk=gameid).exists()
    else:
        player_owns_game = False

    # Check if the developer owns the game and can browse sales statistics for this game
    if hasattr(request.user, 'developer'):
        developer_owns_game = request.user.developer.added_games.filter(pk=gameid).exists()
    else:
        developer_owns_game = False

    # Handle messages coming from the game
    load_data = None
    if hasattr(request.user, 'player') and request.method == 'POST':
        # Player submits a score
        if request.POST.get('score'):
            score_form = ScoreForm(data=request.POST)
            if score_form.is_valid():
                d = score_form.cleaned_data
                HighScore(player=request.user.player, game=game, score=d['score']).save()
        # Player saves a game
        elif request.POST.get('state'):
            save_form = SaveForm(data=request.POST)
            if save_form.is_valid():
                # return redirect(save_form.cleaned_data)
                save_state = save_form.cleaned_data['state']
                SaveState(player=request.user.player, game=game, state=save_state).save()
        # Player loads a game
        elif request.POST.get('request_load'):
            request_load_form = RequestLoadForm(data=request.POST)
            save_states = SaveState.objects.filter(player=request.user.player, game=game)
            if request_load_form.is_valid() and save_states.exists():
                game_state = save_states.latest('pk').state  # Load the latest save
                load_data = '{"messageType": "LOAD", "gameState":' + game_state + '}'
            else:
                # Send back an error message if the game cannot be loaded
                load_data = '{"messageType": "ERROR", "info": "Gamestate could not be loaded"}'

    return render(request, 'gameplay.html',
                  {'game': game, 'player_owns_game': player_owns_game, 'developer_owns_game': developer_owns_game,
                   'load_data': load_data})


def gamelist(request):
    """Browse games view. (Homeview)"""

    # Set all games to be rended in case search requests fail
    games = Game.objects.all()

    # Take search requests to filter the games
    if request.method == 'GET':
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            d = search_form.cleaned_data
            # Filter by game category
            if d['category']:
                if d['category'] in settings.GAME_CATEGORIES:
                    games = games.filter(category=d['category'])
            # Filter game by name
            elif d['name']:
                games = games.filter(name__icontains=d['name'])

    return render(request, 'gamelist.html', {
        'categories': settings.GAME_CATEGORIES,
        'games': games})


@login_required(login_url='/login/')
def add_game(request):
    """View to a form where developers can add more games to the gamestore."""
    if not request.user.has_perm('gamestore.developer'):
        return permission_denied(request, PermissionDenied)

    # Validate the form and add a new game to the database
    new_game = None
    if request.method == 'POST':
        game_form = GameForm(request.POST)
        if game_form.is_valid():
            d = game_form.cleaned_data
            # Check that category is from the predefined list
            if d['category'] not in settings.GAME_CATEGORIES:
                return render(request, 'addgame.html', {
                    'msg': 'Please select a category from the list!',
                    'categories': settings.GAME_CATEGORIES
                })
            developer = Developer.objects.get(user=request.user)
            new_game = Game(name=d['name'], category=d['category'], description=d['description'],
                            game_url=d['game_url'], price=d['price'], developer=developer)
            new_game.save()

    return render(request, 'addgame.html', {
        'new_game': new_game,
        'categories': settings.GAME_CATEGORIES
    })


def register_view(request):
    """Reqister a new user. Creates a new user and user profile (player or developer). Sends an verification email to
    the user. The new user is validated and can login after the user goes to the link provided in the email.
    """
    # Validate the form and create new user and user profile
    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            d = register_form.cleaned_data

            # Check if the typed passwords match each other
            if d['password'] != d['password_check']:
                return render(request, 'register.html', {
                    'message': 'Passwords must match!',
                    'username': d['username'],
                    'first_name': d['first_name'],
                    'last_name': d['last_name'],
                    'email': d['email'],
                    'account_type': d['account_type']
                })

            # Check if the username already exists
            if User.objects.filter(username=d['username']).exists():
                return render(request, 'register.html', {
                    'message': 'Username "' + d['username'] + '" already exists!',
                    'first_name': d['first_name'],
                    'last_name': d['last_name'],
                    'email': d['email'],
                    'account_type': d['account_type']
                })

            # Create a new user
            user = User.objects.create_user(username=d['username'], password=d['password'])
            user.first_name = d['first_name']
            user.last_name = d['last_name']
            user.email = d['email']
            account_type = d['account_type']

            # Create user profile (player or developer) and set user permissions
            model = Player if account_type == 'player' else Developer
            content_type = ContentType.objects.get_for_model(model)
            permission = Permission.objects.get(codename=account_type, content_type=content_type)
            user.user_permissions.add(permission)
            user.save()

            # Set an unique user_hash to the user for email verification
            profile = Player.create(user) if account_type == 'player' else Developer.create(user)
            m = md5(user.username.encode('ascii'))
            userhash = m.hexdigest()
            profile.user_hash = userhash
            profile.save()

            # Compose and send a verification email to the user
            from_email = settings.EMAIL_HOST_USER
            to_email = [from_email, d['email']]
            email_msg = 'Welcome to the GameStore service, ' + d['username'] + \
                        '! \nHere is your email validation link to activate your account. Visit the link to be able' \
                        ' to log in to your account and play the awesome games and compete with other players! \n\n'
            email_msg += request.build_absolute_uri('activate/' + userhash)
            send_mail('Verification code', email_msg, from_email, to_email, fail_silently=False)

            return redirect('/login/?activation_sent=' + d['email'])

    return render(request, 'register.html')


def activate_view(request, user_hash):
    """View registration validation. Unique links to this page are provided in verification emails sent to users after
    registration. The link is created using user_hash, which is stored in users player/developer profiles. This view
    checks if the received user_hash matches a user_hash of a user that is trying to validate his/her account.
    """
    # Search for user_hash in player profiles
    if Player.objects.filter(user_hash=user_hash).exists():
        profile = Player.objects.get(user_hash=user_hash)
        if profile.activated:
            # The profile has been already activated
            return redirect('/login/?activation=duplicate')
        profile.activated = True
        profile.save()
        return redirect('/login/?activation=success')
    # Search for user_hash in developer profiles
    elif Developer.objects.filter(user_hash=user_hash).exists():
        profile = Developer.objects.get(user_hash=user_hash)
        if profile.activated:
            # The profile has been already activated
            return redirect('/login/?activation=duplicate')
        profile.activated = True
        profile.save()
        return redirect('/login/?activation=success')

    # Invalid user_hash
    return redirect('/login/?activation=fail')


def login_view(request):
    """Login view. Validates the login credentials and checks if the account is validated. Also handles 'next' GET
    requests.
    """
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            d = login_form.cleaned_data
            user = authenticate(username=d['username'], password=d['password'])
            if user is not None:
                # Check if the account has been activated through email
                if hasattr(user, 'player'):
                    if not user.player.activated:
                        return redirect('/login/?activated=fail')
                elif hasattr(user, 'developer'):
                    if not user.developer.activated:
                        return redirect('/login/?activated=fail')
                else:
                    # The user is not player or developer. Should not happen.
                    return bad_request(request, BadRequest)

                login(request, user)

                # Check if there was a 'next' GET request (redirect to (previous) page after login)
                if request.POST.get('next'):
                    return redirect(request.POST.get('next'))
                return redirect('/')

    return render(request, 'login.html')


def logout_view(request):
    """A simple logout view."""
    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def account(request):
    """A view for users account page where you can edit your name and password and view owned games etc."""
    # Get owned games for players and added games for developers.
    if hasattr(request.user, 'player'):
        account_type = 'Player'
        games = request.user.player.owned_games.all()
    else:
        account_type = 'Developer'
        games = request.user.developer.added_games.all()

    return render(request, 'account.html', {'account_type': account_type, 'games': games})


@login_required(login_url='/login/')
def edit_name(request):
    """A view to edit the users first and last name."""
    # Validate the edit form and save the new first and last name
    if request.method == 'POST':
        edit_user_form = EditNameForm(request.POST)
        if edit_user_form.is_valid():
            d = edit_user_form.cleaned_data
            request.user.first_name = d['first_name']
            request.user.last_name = d['last_name']
            request.user.save()
            return redirect('/account/')

    return render(request, 'edit_name.html')


@login_required(login_url='/login/')
def edit_password(request):
    """A view to change the users password."""
    # Validate the edit form and save the new password. Also auto re-authenticates the user.
    if request.method == 'POST':
        edit_password_form = EditPasswordForm(request.POST)
        if edit_password_form.is_valid():
            d = edit_password_form.cleaned_data
            if d['password'] == d['password_check'] and request.user.check_password(d['old_password']):
                request.user.set_password(d['password'])
                request.user.save()
                # Re-authenticate the user
                update_session_auth_hash(request, request.user)
                return redirect('/account/')

    return render(request, 'edit_password.html')


@login_required(login_url='/login/')
def edit_game(request, gameid):
    """Edit game information. Only developers can edit their own games."""
    # Check if the user is a developer
    if not request.user.has_perm('gamestore.developer'):
        return permission_denied(request, PermissionDenied)

    # The game to be edited
    game = Game.objects.get(pk=gameid)
    # Check if the developer owns the game
    if not request.user.developer.added_games.filter(pk=gameid).exists():
        return permission_denied(request, PermissionDenied)

    # Validate the edit form and save the changes
    if request.method == 'POST':
        edit_game_form = EditGameForm(request.POST)
        if edit_game_form.is_valid():
            d = edit_game_form.cleaned_data
            game.name = d['name']
            game.category = d['category']
            game.description = d['description']
            game.price = d['price']
            game.save()
            return redirect('/account/')

    return render(request, 'edit_game.html', {'game': game})


@login_required(login_url='/login/')
def sales(request, gameid):
    """A view to check sales statistics. Only developers can check sales statistics for their own games."""
    game = Game.objects.get(pk=gameid)
    orders = Order.objects.filter(game=game, status=True)
    return render(request, 'sales.html', {'game': game, 'orders': orders})


@login_required(login_url='/login/')
def buy_game(request, gameid):
    """A view where players can buy a new game. Creates a new Order-object and prepares parameters for the mockup
    payment service.
    """
    # Check if the user is a player
    if not request.user.has_perm('gamestore.player'):
        return permission_denied(request, PermissionDenied)

    # Check if the player already owns the game
    if request.user.player.owned_games.filter(pk=gameid).exists():
        return permission_denied(request, PermissionDenied)

    # Free games cannot be bought
    game = Game.objects.get(pk=gameid)
    if game.price == 0:
        return permission_denied(request, PermissionDenied)

    # Create a new order object
    order = Order(buyer=request.user.player, seller=game.developer, game=game, price=game.price)
    order.save()
    pid = order.pk

    # Calculate checksum for the payment service
    sid = settings.SID
    checksumstr = 'pid={}&sid={}&amount={}&token={}'.format(pid, sid, game.price, settings.SID_SECRET_KEY)
    m = md5(checksumstr.encode('ascii'))
    checksum = m.hexdigest()

    return render(request, 'buygame.html', {
        'checksum': checksum,
        'pid': pid,
        'sid': sid,
        'game_price': game.price,
        'game_name': game.name
    })


@login_required(login_url='/login/')
def payment_successful(request):
    """A view for receiving and handling successful payments for bought games. Validates the payment using checksum from
    the mockup payment service.
    """
    # Check if the user is a player
    if not request.user.has_perm('gamestore.player'):
        return permission_denied(request, PermissionDenied)

    result = request.GET.get('result')  # success/cancel/error, should be success
    pid = request.GET.get('pid')  # payment id (order pk)
    ref = request.GET.get('ref')  # reference number in the payment number
    checksum1 = request.GET.get('checksum')

    # Check if the result message is correct
    if result != 'success':
        return bad_request(request, BadRequest)

    # Create checksum2 to test if the purchase is valid
    checksumstr = 'pid={}&ref={}&result={}&token={}'.format(pid, ref, result, settings.SID_SECRET_KEY)
    # checksumstr is the string concatenated above
    m = md5(checksumstr.encode('ascii'))
    checksum2 = m.hexdigest()

    # Stop the purchase process if the payment was not valid
    if checksum1 != checksum2:
        return bad_request(request, BadRequest)

    # The purchase process was valid, finalize the order by changing the status of the order to True
    order = Order.objects.get(pk=pid)
    order.status = True
    order.save()
    game = Game.objects.get(pk=order.game.pk)
    request.user.player.owned_games.add(game)

    return render(request, 'post_payment.html', {'state': result, 'order': order, 'game': game})


@login_required(login_url='/login/')
def payment_cancel(request):
    """A view for handling cancelled payments when purchasing a game."""
    # Check if the user is a player
    if not request.user.has_perm('gamestore.player'):
        return permission_denied(request, PermissionDenied)

    # Check if the result message is correct
    result = request.GET.get('result')  # success/cancel/error, should be cancel
    if result != 'cancel':
        return bad_request(request, BadRequest)

    return render(request, 'post_payment.html', {'state': result})


@login_required(login_url='/login/')
def payment_error(request):
    """A view for handling errors in payments when purchasing a game."""
    # Check if the user is a player
    if not request.user.has_perm('gamestore.player'):
        return permission_denied(request, PermissionDenied)

    # Check if the result message is correct
    result = request.GET.get('result')  # success/cancel/error, should be error
    if result != 'error':
        return bad_request(request, BadRequest)

    return render(request, 'post_payment.html', {'state': result})


def high_scores(request, gameid):
    """A view for displaying high scores for a game."""
    game = Game.objects.get(pk=gameid)
    scores = HighScore.objects.filter(game=game)
    return render(request, 'highscores.html', {'scores': scores, 'game': game})


def rest_info(request):
    """A view for rendering RESTful API welcome page."""
    return render(request, 'rest_info.html')


def rest_high_scores(request):
    """A view for RESTful API for fetching high score data."""
    highscores = HighScore.objects.all()
    if request.method == 'GET':
        # Filter by name of the game
        if 'game' in request.GET:
            if Game.objects.filter(name=request.GET['game']).exists():
                game = Game.objects.get(name=request.GET['game'])
                highscores = highscores.filter(game=game)
            else:
                highscores = []

    # Convert player ids to usernames and game ids to game names
    data = serializers.serialize('json', highscores)
    data_json = json.loads(data)
    for d in data_json:
        d['fields']['player'] = Player.objects.get(pk=d['fields']['player']).user.username
        d['fields']['game'] = Game.objects.get(pk=d['fields']['game']).name
        # Remove model information from the returned data
        d.pop('model')
    data = json.dumps(data_json)

    return render(request, 'rest_highscores.html', {'data': data})


def rest_sales(request):
    """A view for RESTful API for fetching sales statistic data. Only developers can fetch sales statistic data for
    their own games.
    """
    # Check if the user is a developer
    if not request.user.has_perm('gamestore.developer'):
        return permission_denied(request, PermissionDenied)

    # Allow only requests for the developers own sales statistics
    orders = request.user.developer.sales.all()

    if request.method == 'GET':
        # Filter by order id
        if 'order' in request.GET:
            orders = orders.filter(pk=request.GET['order'])
        # Filter by game name
        if 'game' in request.GET:
            if Game.objects.filter(name=request.GET['game']).exists():
                game = Game.objects.get(name=request.GET['game'])
                orders = orders.filter(game=game)
            else:
                orders = []
        # Filter by buyer (username in this case!)
        if 'buyer' in request.GET:
            if User.objects.filter(username=request.GET['buyer']).exists():
                user = User.objects.get(username=request.GET['buyer'])
                if hasattr(user, 'player'):
                    orders = orders.filter(buyer=user.player)
                else:
                    orders = []
            else:
                orders = []
        # Search by status (paid or not paid orders)
        if 'status' in request.GET:
            if request.GET['status'] == 'paid':
                orders = orders.filter(status=True)
            elif request.get['status'] == 'not_paid':
                orders = orders.filter(status=False)
            else:
                orders = []

    # Convert buyer and seller ids to usernames and game ids to game names and status to paid/not_paid
    data = serializers.serialize('json', orders)
    data_json = json.loads(data)
    for d in data_json:
        d['fields']['buyer'] = Player.objects.get(pk=d['fields']['buyer']).user.username
        d['fields']['seller'] = Developer.objects.get(pk=d['fields']['seller']).user.username
        d['fields']['game'] = Game.objects.get(pk=d['fields']['game']).name
        d['fields']['status'] = 'paid' if Order.objects.get(pk=d['pk']).status else 'not_paid'
        # Remove model information from the returned data
        d.pop('model')
    data = json.dumps(data_json)

    return render(request, 'rest_sales.html', {'data': data})


def rest_games(request):
    """A view for RESTful API for fetching game data."""
    games = Game.objects.all()
    if request.method == 'GET':
        if 'category' in request.GET:
            # Filter by game category
            games = games.filter(category=request.GET['category'])
        if 'developer' in request.GET:
            # Filter by developer (username in this case!)
            if User.objects.filter(username=request.GET['developer']).exists():
                user = User.objects.get(username=request.GET['developer'])
                if hasattr(user, 'developer'):
                    games = games.filter(developer=user.developer)
                else:
                    games = []
            else:
                games = []

    # Convert developer ids to usernames
    data = serializers.serialize('json', games)
    data_json = json.loads(data)
    for d in data_json:
        d['fields']['developer'] = Developer.objects.get(pk=d['fields']['developer']).user.username
        # Remove model information from the returned data
        d.pop('model')
    data = json.dumps(data_json)

    return render(request, 'rest_games.html', {'data': data})
