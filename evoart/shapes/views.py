# Create your views here.
# Python
import urllib
import urlparse
import oauth2 as oauth
import cgi, json
import datetime


# Django
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

# Project
from shapes import models
from shapes.models import Collection, User_Collection, Collection_Individual
from lib.evospace import Population, Individual
from lib.colors import init_pop, evolve


# It's probably a good idea to put your consumer's OAuth token and
# OAuth secret into your project's settings. 
consumer = oauth.Consumer(settings.TWITTER_TOKEN, settings.TWITTER_SECRET)
client = oauth.Client(consumer)

request_token_url = 'https://api.twitter.com/oauth/request_token'
access_token_url = 'https://api.twitter.com/oauth/access_token'

# This is the slightly different URL used to authenticate/authorize.
#authenticate_url = 'http://twitter.com/oauth/authenticate'
authenticate_url = 'https://api.twitter.com/oauth/authorize'

popName='pop'

@csrf_exempt
def evospace(request):
    if  request.method == 'POST':
            population = Population(popName)
            print 'Raw Data___: "%s"' % request.body
            print type(request.body)
            json_data = json.loads(request.body)
            method = json_data["method"]
            params = json_data["params"]
            id     = json_data["id"]
            
            if method == "initialize":

                result = population.initialize()
                data = json.dumps({"result" : result,"error": None, "id": id})
                print data
                return HttpResponse(data, mimetype='application/javascript')
            elif method == "getSample":
                result = population.get_sample(params[0])
                if result:
                    data = json.dumps({"result" : result,"error": None, "id": id})
                else:
                    data = json.dumps({"result" : None,"error":
                                        {"code": -32601, "message": "EvoSpace empty"}, "id": id})    
                return HttpResponse(data, mimetype='application/json')
            elif method == "putSample":
                data = population.put_sample(params[0]) 
                return HttpResponse(json.dumps("Success"), mimetype='application/json')           
            elif method == "init_pop":
                data = init_pop(populationSize=params[0],evospace_URL= 'http://app.evospace.org/EvoSpace')
                return HttpResponse(json.dumps("Success"), mimetype='application/javascript')
            elif method == "evolve":
                data = evolve(sample_size=params[0],evospace_URL= 'http://app.evospace.org/EvoSpace')
                return HttpResponse(json.dumps("Success"), mimetype='application/javascript')
            elif method == "respawn":
                data = population.respawn(n=params[0])
                return HttpResponse(json.dumps("Success"), mimetype='application/javascript')
            elif method == "put_individual":
                print  "params",params[0]
                population.put_individual(**params[0])
                data = json.dumps({"result" : None,"error": None, "id": id})
                return HttpResponse(data, mimetype='application/json')


    else:
        return HttpResponse("ajax & post please", mimetype='text')
            
#@ensure_csrf_cookie            
def home(request):
    return render_to_response('django_index.html', {'static_server': 'http://evospace.org/prototype/',
      'api_server':'http://app.evospace.org'},context_instance=RequestContext(request) )



def individual_view(request,individual_id):
    key = "pop:individual:%s" % (individual_id)
    individual =  Individual(id=key).get(as_dict=True)
    mama = None
    papa = None
    if "mama" in individual:
        mama = Individual(id=individual["mama"]).get(as_dict=True)

    if "papa" in individual:
        papa = Individual(id=individual["papa"]).get(as_dict=True)

    print "ppppp", papa , mama
    individual_json = json.dumps(individual)

    return render_to_response('individual.html', {'static_server': 'http://evospace.org/prototype/',
      'api_server':'http://app.evospace.org', 'individual':individual_json,'mama':mama,'papa':papa},context_instance=RequestContext(request) )




FaceConsumer = oauth.Consumer(	"503596062988426", "8b39861e5965f5879c90daf607e0a5f0")
FaceClient = oauth.Client(consumer)

def facebook_get_login(request):
    state = request.session.session_key
    url = """https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&state=%s""" % \
              ("503596062988426" ,"http://app.evospace.org/facebook/login/",
               state
                )

    return HttpResponseRedirect(url)

def facebook_login(request):
    error = None

    if 'error' in request:
        raise Exception("Invalid response from Facebook.")
    code = request.GET['code']
    UID = request.GET['state']

    args = { "client_id" : "503596062988426",
            "redirect_uri" : "http://app.evospace.org/facebook/login/" ,
            "client_secret" : "8b39861e5965f5879c90daf607e0a5f0",
            "code" : code }

    response = urllib.urlopen( "https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(args))
    response = urlparse.parse_qs(response.read())
    access_token = response["access_token"][-1]
    profile = json.load(urllib.urlopen(
        "https://graph.facebook.com/me?" +
        urllib.urlencode(dict(access_token=access_token))))
    expires = response['expires'][0]

    facebook_session = models.FacebookSession.objects.get_or_create(
        access_token=access_token)[0]

    facebook_session.expires = expires
    facebook_session.save()

    user = authenticate(token=access_token)
    if user:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            error = 'AUTH_DISABLED'

    if 'error_reason' in request.GET:
        error = 'AUTH_DENIED'

    return HttpResponse(profile["id"]+"-@@@@@@@@-"+profile["username"]+"----" +profile["name"]+"  expira en:"+response["expires"][-1]+error)



def twitter_login(request):
    # Step 1. Get a request token from Twitter.
    resp, content = client.request(request_token_url, "GET")
    print content
    if resp['status'] != '200':
        raise Exception("Invalid response from Twitter.")

    # Step 2. Store the request token in a session for later use.
    request.session['request_token'] = dict(cgi.parse_qsl(content))

    # Step 3. Redirect the user to the authentication URL.
    url = "%s?oauth_token=%s" % (authenticate_url,
        request.session['request_token']['oauth_token'][-1])

    return HttpResponseRedirect(url)


@login_required
def logout_view(request):
    # Log a user out using Django's logout function and redirect them
    # back to the homepage.
    logout(request)
    return HttpResponseRedirect('/')

def twitter_authenticated(request):
    # Step 1. Use the request token in the session to build a new client.
    token = oauth.Token(request.session['request_token']['oauth_token'],
        request.session['request_token']['oauth_token_secret'])
    client = oauth.Client(consumer, token)

    # Step 2. Request the authorized access token from Twitter.
    resp, content = client.request(access_token_url, "GET")
    if resp['status'] != '200':
        print content
        raise Exception("Invalid response from Twitter.")

    """
    This is what you'll get back from Twitter. Note that it includes the
    user's user_id and screen_name.
    {
        'oauth_token_secret': 'IcJXPiJh8be3BjDWW50uCY31chyhsMHEhqJVsphC3M',
        'user_id': '120889797', 
        'oauth_token': '120889797-H5zNnM3qE0iFoTTpNEHIz3noL9FKzXiOxwtnyVOD',
        'screen_name': 'heyismysiteup'
    }
    """
    access_token = dict(cgi.parse_qsl(content))

    # Step 3. Lookup the user or create them if they don't exist.
    try:
        user = User.objects.get(username=access_token['screen_name'])
    except User.DoesNotExist:
        # When creating the user I just use their screen_name@twitter.com
        # for their email and the oauth_token_secret for their password.
        # These two things will likely never be used. Alternatively, you 
        # can prompt them for their email here. Either way, the password 
        # should never be used.
        user = User.objects.create_user(access_token['screen_name'],
            '%s@twitter.com' % access_token['screen_name'],
            access_token['oauth_token_secret'])

        # Save our permanent token and secret for later.
        profile = Profile()
        profile.user = user
        profile.oauth_token = access_token['oauth_token']
        profile.oauth_secret = access_token['oauth_token_secret']
        profile.save()

    # Authenticate the user and log them in using Django's pre-built 
    # functions for these things.
    user = authenticate(username=access_token['screen_name'],
        password=access_token['oauth_token_secret'])
    login(request, user)

    return HttpResponseRedirect('/')

@csrf_exempt
def add_collection(request, username):
    global message
    errors = []
    if request.method == 'POST':

        #users=User.objects.all();
        u1=User.objects.get(username=username)
        #u=users[0]

        n=request.POST['name']
        d=request.POST['description']
        v=request.POST['visibility']

        c = Collection(name=n,
            description=d,
            creation_date=datetime.datetime.now(),
            visibility=v
        )
        c.save()
        c_id=Collection.objects.latest('id')
        c_id=c_id.id
        u_id=u1.id

        if User.objects.get(id=u_id) and Collection.objects.get(id=c_id):
            u=User.objects.get(id=u_id)
            c=Collection.objects.get(id=c_id)
            uc= User_Collection(user=u,
                collection=c,
                role="O",
                status="PU"
            )
            uc.save()
            message= "You are now linked to this collection!"
        else:
            message= "Sorry there is no collection or user"
            #add_user_collection(id,c_id)
        col= Collection.objects.all()

        data=({'name':n,'description':d,'visibility':v, 'message':message})
        datar=json.dumps(data)


    return HttpResponse(datar, mimetype='application/json')

def get_user_collections(request, username):

    if User.objects.get(username=username):
        u1=User.objects.get(username=username)
        u_id=u1.id
        uc=Collection.objects.all().filter(user_collection__user_id__exact=u_id)
        jd = { 'collections': [{'id': col.id, 'name':col.name} for col in uc]}
        j=json.dumps(jd)


    return HttpResponse(j, mimetype='application/json')

@csrf_exempt
def add_ind_to_col(request, username):
    global message
    if request.method == 'POST':

        if  User.objects.get(username=username):

            u1=User.objects.get(username=username)
            u=User.objects.get(id=u1.id)



            col=request.POST['collection']
            ind=request.POST['individual']

            c=Collection.objects.get(id=col)

            itc=Collection_Individual( collection=c,
                 individual_id=ind,
                 added_from=c,
                 from_user=u,
                 date_added=datetime.datetime.now())

            itc.save()
            message="Individual is now added to this collection!"
        else:
            message="No username in evoart!"


        data=({'collection':col,'individual':ind, 'message':message})
        datar=json.dumps(data)


    return HttpResponse(datar, mimetype='application/json')


