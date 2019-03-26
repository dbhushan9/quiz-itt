import random
import string
from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


from random import choice
from string import ascii_lowercase, digits
from django.contrib.auth.models import User

def generate_random_username(length=4, chars=digits, split=4, delimiter='',exam='Exam'):
    username = ''.join([choice(chars) for i in range(length)])
    if split:
        username = delimiter.join([username[start:start+split] for start in range(0, len(username), split)])

    try:
        user_name = exam+'_user'+username
        User.objects.get(username=user_name)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter,exam=exam)
    except User.DoesNotExist:
        return exam+'_user'+username;


''''
#Random password generator
for user in new_users:
    password = User.objects.make_random_password()
    user.set_password(password)
    # email/print password
'''
