from babtyno.models import HomePage
def get_site_password():
    #Return the site passsword or none (handle none in template)
    #Relies on there being a page with the slug 'home'
    try:
        hp_pwd = HomePage.objects.get(slug='home')[0]
        return hp_pwd.get_view_restrictions().values_list('password',flat=True)[0]
    except HomePage.DoesNotExist:
        return ''
