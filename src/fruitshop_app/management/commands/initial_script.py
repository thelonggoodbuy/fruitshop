from django.core.management.base import BaseCommand
import random


from django.contrib.auth.models import User
from fruitshop_app.models import Message, Commodity, Account


class Command(BaseCommand):
    '''
    Script check, and if It necessary create such objects:
    1. 6 type of Fruit commodity(pineapple, apple, banana, orange, peach, kiwi)
    2. 1 account object
    3. 4 user (2 simple, 1 tehcsupport and 1 joker)
    '''
    help = "Initialisation of all needfull objects, for app working"

    def handle(self, *args, **kwargs):
        # create fruit commodity
        dict_of_fruits = {'pineapple': 'aнанас','apple': 'яблуко',
                          'banana': 'банан', 'orange': 'апельсин', 
                          'peach': 'персик', 'kiwi': 'ківі'}
        
        simple_users_list = ['initial_user_1', 'initial_user_2']
        initial_password = 'initial_password123!'
        created_objects_list = []
        utility_usernames = ['techsupport', 'joker']
        

        for fruit_raw_title in dict_of_fruits.keys():
            fruit_obj, created = Commodity.objects.get_or_create(
                title=dict_of_fruits[fruit_raw_title],
                raw_title=fruit_raw_title
                )
            if created: 
                fruit_obj.quantity = 25
                fruit_obj.save()
                created_objects_list.append(f"Commodity {fruit_obj.raw_title}.")

        # create account
        account = Account.objects.first()
        if account is None:
            account = Account.objects.create(total_debt=5000)
            created_objects_list.append("Bank account with 5000$ ")

        # create techsupport
        techsupport_obj, created = User.objects.get_or_create(
                username='techsupport',
                last_name='технічна підтримка'
                )
        if created:
            techsupport_obj.set_password(initial_password)
            techsupport_obj.save()
            created_objects_list.append("User for Techsupport")

        # create jocker
        joker_obj, created = User.objects.get_or_create(
                username='joker',
                last_name='жартівник'
                )
        if created:
            joker_obj.set_password(initial_password)
            joker_obj.save()
            created_objects_list.append("User for Jokes")

        # create two simple users
        if User.objects.filter().exclude(username__in=utility_usernames).count() < 2:
            for username in simple_users_list:
                new_user = User.objects.create(username=username)
                new_user.set_password(initial_password)
                new_user.save()
                created_objects_list.append(f"User with username {new_user.username}")

        # create admin  users       
        admin_user_obj, created = User.objects.get_or_create(
                username='initial_admin',
                last_name='технічна підтримка'
                )
        if created:
            admin_user_obj.set_password(initial_password)
            admin_user_obj.is_superuser = True
            admin_user_obj.is_staff = True
            admin_user_obj.is_active = True
            admin_user_obj.save()
            created_objects_list.append("Initial Admin user")




        # send list of created objects to terminal
        if len(created_objects_list) > 0:
            print('----------Objects-created-by-initial-script----------')
            for created_obj in created_objects_list:
                print(created_obj)
            print('----------------------------------------------------')

        else:
            print('----------All needfull objects already exist in DB----------')
