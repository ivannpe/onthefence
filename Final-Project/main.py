#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import random
import webapp2
import json
import urllib
import urllib2
import jinja2
import os
import time
import logging
from google.appengine.ext import ndb
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Person(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    profile_image = ndb.StringProperty()
    restaurants = ndb.StringProperty(repeated = True)
    entertainments = ndb.StringProperty(repeated = True)
    outdoors = ndb.StringProperty(repeated = True)
    indoors = ndb.StringProperty(repeated = True)
    home = ndb.StringProperty(repeated = True)
    location = ndb.StringProperty()
    age = ndb.StringProperty()

class Feedback(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    feedback = ndb.StringProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        people = Person.query().fetch()
        in_people = False
        check = True
        if user:
            for person in people:
                if user.nickname() == person.email:
                    in_people = True
            if in_people == False:
                current_user = Person(name=user.nickname(), email=user.nickname(), profile_image="https://static.tplugin.com/tplugin/img/unknown-user.png",
                    restaurants=[], entertainments=[], outdoors=[], indoors=[], home=[], location=" ", age=" ")
                current_user.put()
            else:
                for person in people:
                    if person.email == user.nickname():
                        current_user = person
            greeting = ('Welcome, %s!' %
                (current_user.name))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                users.create_login_url('/'))
            check = False
        template = jinja_environment.get_template('templates/onthefence.html')
        vars_dict = {'response': greeting, 'check': check}
        self.response.out.write(template.render(vars_dict))

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        logout = users.create_logout_url('/')
        key = self.request.get('key')
        user = users.get_current_user()
        people = Person.query().fetch()
        if key:
            person_key = ndb.Key(urlsafe=key)
            current_person = person_key.get()
        else:
            for person in people:
                if user.nickname() == person.email:
                    current_person = person
        vars_dict = {'name': current_person.name, 'restaurant_list': current_person.restaurants, 'entertainment_list': current_person.entertainments,
            'outdoors_list': current_person.outdoors, 'indoors_list': current_person.indoors,'home_list': current_person.home, 'url': logout,
            'location': current_person.location, 'age': current_person.age, 'photo_url': current_person.profile_image}
        template = jinja_environment.get_template("templates/profile-page.html")
        self.response.write(template.render(vars_dict))

    def post(self):
        user = users.get_current_user()
        person = Person.query(Person.email == user.nickname()).fetch()[0]
        category = self.request.get("category")
        # new_restaurant = Restaurant(name = self.request.get('food'))
        # if new_restaurant.name != "":
        #     new_restaurant.put()
        # restaurants = Restaurant.query().fetch()
        # restaurant_list = []
        # for place in restaurants:
        #     restaurant_list.append(place.name)
        # if new_restaurant.name not in restaurant_list and new_restaurant.name != "":
        #     restaurant_list.append(new_restaurant.name)

        if category == "restaurants":

            new_restaurant = self.request.get('input')
            if new_restaurant not in person.restaurants and new_restaurant != "":
                person.restaurants.append(new_restaurant)

                person.put()
        # new_entertainment = Entertainment(name = self.request.get('entertainment'))
        # if new_entertainment.name != "":
        #     new_entertainment.put()
        # entertainments = Entertainment.query().fetch()
        # entertainment_list = []
        # for place in entertainments:
        #     entertainment_list.append(place.name)

        if category == "entertainment":

            new_entertainment = self.request.get('input')
            if new_entertainment not in person.entertainments and new_entertainment != "":
                person.entertainments.append(new_entertainment)

            person.put()

        if category == "outdoors":

            new_outdoors = self.request.get('input')
            if new_outdoors not in person.outdoors and new_outdoors != "":
                person.outdoors.append(new_outdoors)
            person.put()

        if category == "indoors":

            new_indoors = self.request.get('input')
            if new_indoors not in person.indoors and new_indoors != "":
                 person.indoors.append(new_indoors)
            person.put()

        if category == "home":


            new_home = self.request.get('input')
            if new_home not in person.home and new_home != "":
                 person.home.append(new_home)
            person.put()

        # vars_dict = {'name': person.name, 'restaurant_list': person.restaurants, 'entertainment_list': person.entertainments,
        #     'outdoors_list': person.outdoors, 'indoors_list': person.indoors,'home_list': person.home,
        #     'location': person.location, 'age': person.age, 'photo_url': person.profile_image}
        # template = jinja_environment.get_template("templates/profile-page.html")
        # self.response.write(template.render(vars_dict))


class Randomizer(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/randomizer.html")
        self.response.write(template.render())
    def post(self):
        user = users.get_current_user()
        person = Person.query(Person.email == user.nickname()).fetch()[0]
        random_place = ''
        template = jinja_environment.get_template("templates/randomizer.html")
        # restaurants = Restaurant.query().fetch()
        # restaurant_list = []
        # for place in restaurants:
        #     restaurant_list.append(place.name)
        if self.request.get('category_answer') == 'Food':
            random_place = (random.choice(person.restaurants))
        elif self.request.get('category_answer') == 'Entertainment':
            random_place = (random.choice(person.entertainments))
        elif self.request.get('category_answer') == 'Outdoors':
            random_place = (random.choice(person.outdoors))
        elif self.request.get('category_answer') == 'Indoors':
            random_place = (random.choice(person.indoors))
        elif self.request.get('category_answer') == 'Home':
            random_place = (random.choice(person.home))
        vars_dict = {'random':random_place}
        self.response.write(template.render(vars_dict))

class EditPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/profilepage.html")
        self.response.write(template.render())
    def post(self):
        user = users.get_current_user()
        person = Person.query(Person.email == user.nickname()).fetch()[0]
        name = self.request.get("name")
        if name != "":
            person.name = name
        age = self.request.get("age")
        if age != "":
            person.age = age
        location = self.request.get("location")
        if location != "":
            person.location = location
        picture = self.request.get("picture")
        if picture != "":
            person.profile_image = picture
        person.put()
        time.sleep(.1)
        self.redirect('/profile?key=%s' % person.key.urlsafe())

class ApiRandom(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/randomizerus.html')
        self.response.write(template.render())
    def post(self):
        random_place = ''
        template = jinja_environment.get_template('templates/randomizerans.html')
        user_search = {
        'category_answer' : self.request.get('category'),
        'location_answer' : self.request.get('location').replace(" ", "+")
        }

        # change often
        apikey = '&key=AIzaSyDAEyX_eVXooWfqiKv6JrsouKOOmoaFOXM'
        # AIzaSyAa6IdoDySL4CJUjX_4kA81E2J9CS6jJDY'

        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
        full_url = base_url + user_search["category_answer"] + '+in+' + user_search["location_answer"] + apikey

        search_data = urllib2.urlopen(full_url)
        search_json = search_data.read()
        search_dictionary = json.loads(search_json)
        result_dictionary = {}
        results = search_dictionary["results"]
        new_results = []



        for result in results:
            new_result = {}
            new_result["formatted_address"] = result["formatted_address"]
            new_result["name"] = result["name"]
            new_results.append(new_result)

        result_dictionary["new_results"] = new_results

        # logging.info(result_dictionary)

        random_place = (random.choice(result_dictionary["new_results"]))
        place_name = random_place['name'] + " " + random_place['formatted_address']
        place_name.replace(' ', "%20").replace("&", "%26")
        vars_dict = {'random':random_place, 'place_name': place_name}
        self.response.write(template.render(vars_dict))


class DeleteProfileListInput(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        person = Person.query(Person.email == user.nickname()).fetch()[0]
        cat = self.request.get("category")
        userdata = self.request.get("input").strip()





        if cat == "restaurants":
            restaurants = person.restaurants
            logging.info(restaurants)
            restaurants.remove(userdata)
            person.restaurants = restaurants
            person.put()


        if cat == "entertainment":
            entertainment = person.entertainment
            logging.info(entertainment)
            entertainment.remove(userdata)
            person.entertainment = entertainment
            person.put()

        if cat == "outdoors":
            outdoors = person.outdoors
            logging.info(outdoors)
            outdoors.remove(userdata)
            person.outdoors = outdoors
            person.put()


        if cat == "indoors":
            indoors = person.indoors
            logging.info(indoors)
            indoors.remove(userdata)
            person.indoors = indoors
            person.put()

        if cat == "home":
            home = person.home
            logging.info(home)
            home.remove(home)
            person.home = home
            person.put()

#
class FeedbackPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/feedback.html')
        self.response.write(template.render())
    def post(self):
        new_feedback = Feedback(name="", email = "", feedback = "")
        feedback_name = self.request.get('name')
        if feedback_name != "":
            new_feedback.name = feedback_name
            new_feedback.put()
        feedback_email = self.request.get('email')
        if feedback_email != "":
            new_feedback.email = feedback_email
            new_feedback.put()
        feedback_text = self.request.get('text')
        if feedback_text != "":
            new_feedback.feedback = feedback_text
            new_feedback.put()
        template = jinja_environment.get_template('templates/feedback.html')
        self.response.write(template.render())

class ViewFeedbackPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/viewfeedback.html')
        feedback = Feedback.query().fetch()
        vars_dict = {'feedback': feedback}
        self.response.write(template.render(vars_dict))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/profile', ProfilePage),
    ('/random', Randomizer),
    ('/editprofile', EditPage),
    ('/recommendation', ApiRandom),
    ('/deleteinput', DeleteProfileListInput),
    ('/feedback', FeedbackPage),
    ('/viewfeedback', ViewFeedbackPage)
], debug=True)
