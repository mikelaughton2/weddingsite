# A Django Wedding Website and Invitation + Guest Management System

Based on [django-wedding-website](https://github.com/czue/django-wedding-website) - thank you!

## What's included?

This includes everything we did for our own wedding:

- A responsive, multi-page website
- New: Websites are configurable to be multilingual
- New: Intuitive CMS to make the single-page website more customisable within the template
- A complete guest management application
- New: GUI email framework for sending save the dates to your guests
- New: Customisable save-the-dates and RSVP emails
- New: Some multilingual support for the outward facing website
- New: Email framework for invitations and built-in RSVP system. Emails are responsive and customisable
- New: Models for invitations to send customisable save the dates
- Guest dashboard

More details on these below.

### The "Standard" Wedding Website

The standard wedding website is a responsive, twitter bootstrap-based site (using a modified version of
[this theme](https://blackrockdigital.github.io/startbootstrap-creative/)).

It is completely customisable to your needs and the content is laid out in standard django templates. By default it includes:

- A "hero" splash screen for a photo
- A mobile-friendly top nav with scrollspy
- A photo/hover navigation pane
- Configurable content sections for every aspect of your site that you want within the CMS
- A set of different styles you can use for different sections

![Hero Section of Wedding Website](https://raw.githubusercontent.com/czue/django-wedding-website/master/screenshots/hero-page.png)

### Multilingual websites
Adjust your settings.py file to include something like:

```python
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [

    ('en-gb','English (British)'),
    ('es','Spanish'),
    ('fr','French'),
]
```
Go to settings>locales, add corresponding locales. Sync pages and include translations.

Create multilingual menus - for default site, Main Menu; for translations, Flat Menus with the *handle* containing language code. In the example above, the flat menu would be called ```fr```.

### Guest management

The guest management functionality acts as a central place for you to manage your entire guest list.
It includes two data models - the `Party` and the `Guest`.

#### Party model

The `Party` model allows you to group your guests together for things like sending a single invitation to a couple.
You can also add parties that you're not sure you're going to invite using the `is_invited` field, which works great for sending tiered invitations.
There's also a field to track whether the party is invited to the rehearsal dinner.

#### Guest model

The `Guest` model contains all of your individual guests.
In addition to standard name/email it has fields to represent whether the guest is a child (for kids meals/pricing differences),
and, after sending invitations, marking whether the guest is attending and what meal they are having

#### Excel import/export

The guest list can be imported and exported via excel (csv).
This allows you to build your guest list in Excel and get it into the system in a single step.
It also lets you export the data to share with others or for whatever else you need.

See the `import_guests` management command for more details and `bigday/guests/tests/data` for sample file formats.

### Save the Dates

The app comes with a built-in cross-client and mobile-friendly email template for save the dates (see `save_the_date.html`).

You can create multiple save the dates and send them out either randomly or by `Party` type (useful if you want to send formal
invitations to some people and more playful ones to others).

See `save_the_date.py` and `SAVE_THE_DATE_CONTEXT_MAP` for customizing your save the dates.
PS:  SAVE_THE_DATE_CONTEXT_MAP is now generated from database entries.

### Sending save the dates
The app comes with a very simple interface to send out save the dates when you're done.

Options: test-only, mark-as-sent.

Sending individual ones means going into `django-admin` and importing functions from `save_the_date.py`. Working on that...

### Invitations and RSVPs

The app also comes with a built-in invitation system.
The template is similar to the save-the-date template, however in addition to the standard invitation content it includes:

- A built in tracking pixel to know whether someone has opened the email or not (NB: this doesn't work anymore, I used MailGun instead)
- Unique invitation URLs for each party with pre-populated guest names ([example](http://rownena-and.coryzue.com/invite/b2ad24ec5dbb4694a36ef4ab616264e0/))
- Online RSVP system with meal selection and validation

### Guest dashboard

After your invitations go out you can use the guest dashboard to see how many people have RSVP'd, everyone who still
has to respond, people who haven't selected a meal, etc.
It's a great way of tracking your big picture numbers in terms of how many guests to expect.

Just access `/dashboard/` from an account with admin access. Your other guests won't be able to see it.

![Wedding Dashboard](https://raw.githubusercontent.com/czue/django-wedding-website/master/screenshots/wedding-dashboard.png)
Preview is out of date here

### Other details

You can easily hook up Google analytics by editing the tracking ID in `google-analytics.html`.


## Installation

This is developed for Python 3 and Django 2.2. It works with Django 4.1 as well.

It's recommended that you setup a virtualenv before development.

Then just install requirements, migrate, and runserver to get started:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Customization

I *still* recommend recommend forking this project and just manually modifying it by hand to replace everything with what you want.
Searching for the text on a page in the repository is a great way to find where something lives.

However, in due course I hope that this will be essentially plug-in-and-play.

### Sending email

This application uses Django's email framework for sending mail. 
You need to modify the `EMAIL_HOST`, `EMAIL_PORT` and other associated variables in `settings.py` in order
to hook it into a real server.

Recommend you plug into MailGun, SendGrid, or other type of mail service.

### Email addresses

To customize the email addresses, see the `DEFAULT_WEDDING_FROM_EMAIL` and
`DEFAULT_WEDDING_REPLY_EMAIL` variables in `localsettings.py`.

### Other customizations

If you want to use this project for your wedding but need help getting started just [get in touch](http://www.coryzue.com/contact/) or make an issue
for anything you encounter and I'm happy to help.

I haven't built out more complete customization docs yet because I wasn't sure anyone would be interested in this,
but will add to these instructions whenever I get questions!

-Mike 
-Based on Cory linked above, including liberally borrowing from his README.
