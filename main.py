import random
import datetime

import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Df25012003#!",
    database="sakila"
)

cursor = connection.cursor()


# ..................customer
def signup_customer():
    first_name = input("Enter firstname")
    last_name = input("Enter lastname")
    email = input("Enter email")
    username = input("Enter username")
    password = input("Enter password")
    cursor.execute("insert into customer \n"
                   "(store_id, address_id, first_name, last_name, email, create_date, username, password)\n"
                   "values (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (
                       random.randint(1, 2), random.randint(1, 100), first_name, last_name, email, datetime.datetime.now(), username, password))

    connection.commit()

    cursor.execute("select * from customer")
    results = cursor.fetchall()

    customer_id = None
    for result in results:
        if result[2] == first_name and result[3] == last_name:
            customer_id = result[0]
            break

    return customer_id


def signin_customer():
    username = input("Enter username")
    password = input("Enter password")

    cursor.execute("select * from customer")
    results = cursor.fetchall()

    check = False
    customer_id = None
    for row in results:
        if row[9] == password and row[10] == username:
            customer_id = row[0]
            check = True
            break

    if check is False:
        print("not find")
        exit()

    return customer_id


def view_stores():
    cursor.execute("select store_id, address, city, country\n"
                   "from store, address, city, country\n"
                   "where store.address_id = address.address_id and address.city_id = city.city_id and country.country_id = city.country_id")

    results = cursor.fetchall()

    print("{:<15} {:<25} {:<15} {:<15}".format("store id", "address", "city", "country"))

    for row in results:
        print("{:<15} {:<25} {:<15} {:<15}".format(row[0], row[1], row[2], row[3]))


def view_profile(customer_id):
    cursor.execute("select * from customer")

    results = cursor.fetchall()

    temp = ()
    for row in results:
        if row[0] == customer_id:
            temp = row
            break

    print(f"customer id : {temp[0]}")
    print(f"username : {temp[10]}")
    print(f"firstname : {temp[2]}")
    print(f"lastname : {temp[3]}")
    print(f"email : {temp[4]}")


def edit_profile(customer_id):
    select_option_edit = int(input("Which item do you want to change?\n"
                                   "1.username\n"
                                   "2.password\n"
                                   "3.firstname\n"
                                   "4.lastname\n"
                                   "5.email\n"))
    match select_option_edit:

        case 1:
            new_username = input("Enter new username")
            cursor.execute("update customer\n"
                           f"set username = {new_username}\n"
                           f"where customer_id = {customer_id}")

            connection.commit()

        case 2:
            new_password = input("Enter new password")
            cursor.execute("update customer\n"
                           f"set password = {new_password}\n"
                           f"where customer_id = {customer_id}")

            connection.commit()

        case 3:
            new_firstname = input("Enter new firstname")
            cursor.execute("update customer\n"
                           f"set firstname = {new_firstname}\n"
                           f"where customer_id = {customer_id}")

            connection.commit()

        case 4:
            new_lastname = input("Enter new lastname")
            cursor.execute("update customer\n"
                           f"set lastname = {new_lastname}\n"
                           f"where customer_id = {customer_id}")

            connection.commit()

        case 5:
            new_email = input("Enter new email")
            cursor.execute("update customer\n"
                           f"set email = {new_email}\n"
                           f"where customer_id = {customer_id}")

            connection.commit()


def view_my_rental_movie(customer_id):
    cursor.execute("select rental_date, return_date, title, description\n"
                   "from rental, inventory, film\n"
                   f"where rental.inventory_id = inventory.inventory_id and film.film_id = inventory.film_id and rental.customer_id = {customer_id};")

    results = cursor.fetchall()

    print("{:<15} {:<15} {:<15} {:<25}".format("rental_date", "return_date", "title", "description"))

    for row in results:
        print("{:<15} {:<15} {:<15} {:<25}".format(row[0], row[1], row[2], row[3]))


def request_reservation(customer_id):
    select_film = input("Enter film")

    cursor.execute("select *\n"
                   "from  film\n"
                   f"where title = {select_film}")

    tpl = cursor.fetchall()

    cursor.execute("select *\n"
                   "from inventory, reservation\n"
                   f"where inventory.inventory_id = reservation.inventory_id and film_id = {tpl[0]}\n")

    films = cursor.fetchall()

    if len(films) == 1:

        cursor.execute("select film_id\n"
                       "from film\n"
                       f"where title = {select_film}")

        film_id = cursor.fetchall()

        cursor.execute("select inventory_id\n"
                       "from inventory\n"
                       f"where film_id = {film_id}")

        inventory_id = cursor.fetchall()

        cursor.execute("insert into reservation\n"
                       "(reservation_date, inventory_id, customer_id, return_date) values(%s, %s, %s, %s)",
                       (datetime.datetime.now(), inventory_id, customer_id,
                        datetime.datetime.now() + datetime.timedelta(days=14)))

        print(f"The film of {select_film} has been reserved for you")

    else:
        print("film not fond or film reserved")


def view_my_movies(customer_id):
    cursor.execute("select title, description, rental_date, return_date\n"
                   "from film, inventory, rental\n"
                   f"where film.film_id = inventory.film_id and inventory.inventory_id = rental.inventory_id and rental.customer_id = {customer_id}")

    results = cursor.fetchall()

    print("{:<15} {:<25} {:<15} {:<15}".format("title", "description", "rental_date", "return_date"))

    for row in results:
        print("{:<15} {:<25} {:<15} {:<15}".format(row[0], row[1], row[2], row[3]))


# ..................manager

def signin_manager():
    username = input("Enter username")
    password = input("Enter password")

    cursor.execute("select * from staff")
    results = cursor.fetchall()

    check = False
    staff_id = None
    for row in results:
        if row[9] == password and row[10] == username:
            staff_id = row[0]
            check = True
            break

    if check is False:
        print("not find")
        exit()

    return staff_id


def view_my_customers(staff_id):
    cursor.execute("select first_name, last_name, email\n"
                   "from customer, store\n"
                   f"where customer.store_id = store.store_id and store.manager_staff_id = {staff_id}\n")

    results = cursor.fetchall()

    print("{:<15} {:<15} {:<15}".format("firstname", "lastname", "email"))

    for row in results:
        print("{:<15} {:<15} {:<15%}".format(row[0], row[1], row[2]))


def check_request_reserve(staff_id):

    cursor.execute("select first_name, last_name, email, reservation_date, return_date\n"
                   "from reservation, customer\n"
                   f"where reservation.customer_id = customer.customer_id and reservation.staff_id = {staff_id}")

    results = cursor.fetchall()

    print("{:<15} {:<15} {:<15} {:<15} {:<15}".format("firstname", "lastname", "email", "reservation date", "return date"))

    for row in results:
        print("{:<15} {:<15} {:<15%} {:<15} {:<15}".format(row[0], row[1], row[2], row[3], row[4]))


def register_request(staff_id):
    pass


def view_store_information(staff_id):

    cursor.execute("select store id, address, city, country\n"
                   "from store, address, city, country\n"
                   "where store.address_id = address.address_id and address.city_id = city.city_id and city.country_id = country.country_id \n"
                   f"and store.manager_staff_id = {staff_id}")

    results = cursor.fetchall()

    print("{:<15} {:<25} {:<15} {:<15}".format("store id", "address", "city", "country"))

    for row in results:
        print("{:<15} {:<25} {:<15%} {:<15}".format(row[0], row[1], row[2], row[3]))


def edit_store_information(staff_id):
    pass


# ..................common


def search_movie():
    select = int(
        input("On what basis do you want to search?(1.actor, 2.category, 3.title, 4.language, 5.release year)"))

    match select:

        case 1:
            first_name, last_name = input("Enter actor").split()

            cursor.execute("select first_name, last_name, title, description\n"
                           "from actor, film_actor, film\n"
                           "where actor.actor_id = film_actor.actor_id and film.film_id = film_actor.film_id\n"
                           f"actor.first_name = {first_name} and actor.last_name = {last_name}")

            results = cursor.fetchall()

            print("{:<15} {:<15} {:<15} {:<25}".format("firstname", "lastname", "title", "description"))

            for row in results:
                print("{:<15} {:<15} {:<15} {:<25}".format(row[0], row[1], row[2], row[3]))

        case 2:
            category = input("Enter category")

            cursor.execute("select category.name as category, title, description\n"
                           "from film, film_category, category\n"
                           "where film.film_id = film_category.film_id and film_category.category_id = category.category_id\n"
                           f"and category.name = {category}")

            results = cursor.fetchall()

            print("{:<15} {:<15} {:<25}".format("category", "title", "description"))

            for row in results:
                print("{:<15} {:<15} {:<25}".format(row[0], row[1], row[2]))

        case 3:
            title = input("Enter title")

            cursor.execute("select title, description\n"
                           "from film\n"
                           f"where title = {title}")

            results = cursor.fetchall()

            print("{:<15} {:<25}".format("title", "description"))

            for row in results:
                print("{:<15} {:<25}".format(row[0], row[1]))

        case 4:
            language = input("Enter language")

            cursor.execute("select title, description, name as language\n"
                           "from film, language\n"
                           f"where film.language_id = language.language_id and language.name = {language}")

            results = cursor.fetchall()

            print("{:<15} {:<25} {:<15}".format("title", "description", "language"))

            for row in results:
                print("{:<15} {:<25} {:<15}".format(row[0], row[1], row[2]))

        case 5:
            release_year = input("Enter release year")

            cursor.execute("select title, description, release_year\n"
                           "from film\n"
                           f"where release year = {release_year}")

            results = cursor.fetchall()

            print("{:<15} {:<25} {:<15}".format("title", "description", "release year"))

            for row in results:
                print("{:<15} {:<25} {:<15}".format(row[0], row[1], row[2]))


def view_rental_information(id, role):
    if role == 0:  # customer
        cursor.execute("select title, description, rental_date, return_date\n"
                       "from film, inventory, rental\n"
                       f"where film.film_id = inventory.film_id and inventory.inventory_id = rental.inventory_id and rental.customer_id = {id}\n")

        results = cursor.fetchall()

        print("{:<15} {:<25} {:<15} {:<15}".format("title", "description", "rental date", "return date"))

        for row in results:
            print("{:<15} {:<25} {:<15} {:<15}".format(row[0], row[1], row[2], row[3]))

    else:  # manager
        cursor.execute("select title, description, rental_date, return_date\n"
                       "from film, inventory, rental\n"
                       f"where film.film_id = inventory.film_id and inventory.inventory_id = rental.inventory_id and rental.staff_id = {id}\n")

        results = cursor.fetchall()

        print("{:<15} {:<25} {:<15} {:<15}".format("title", "description", "rental date", "return date"))

        for row in results:
            print("{:<15} {:<25} {:<15} {:<15}".format(row[0], row[1], row[2], row[3]))


def view_list_movie():
    select_category = input("Enter favorite category : \n"
                            "(Action, Animation, Children, Documentary, Drama, Family, Foreign, Games, Horror, Music, New, Sci-Fi, Sports, Travel)\n")

    cursor.execute("select name, title ,description, release_year\n"
                   "from category, film_category, film\n"
                   f"where category.category_id = film_category.category_id and film.film_id = film_category.film_id and name = {select_category};")

    results = cursor.fetchall()

    print("{:<15} {:<15} {:<25} {:<15}".format("category", "title", "description", "release year"))

    for row in results:
        print("{:<15} {:<15} {:<25} {:<15}".format(row[0], row[1], row[2], row[3]))

# ......................................


def menu_customer(customer_id):

    while True:
        select_operation = int(input("select operation: \n"
                                     "1.view stores\n"
                                     "2.view profile\n"
                                     "3.edit profile\n"
                                     "4.view my rental movie\n"
                                     "5.request reservation\n"
                                     "6.view my movies\n"
                                     "7.search movie\n"
                                     "8.view rental information\n"
                                     "9.view list movie\n"
                                     "10.exit\n"))

        match select_operation:

            case 1:
                view_stores()

            case 2:
                view_profile(customer_id)

            case 3:
                edit_profile(customer_id)

            case 4:
                view_my_rental_movie(customer_id)

            case 5:
                request_reservation(customer_id)

            case 6:
                view_my_movies(customer_id)

            case 7:
                search_movie()

            case 8:
                view_rental_information(customer_id, 0)

            case 9:
                view_list_movie()

            case 10:
                exit()

        print("-------------------------------------------------------------------")


def menu_manager(staff_id):

    while True:
        select_operation = int(input("select operation: \n"
                                     "1.view my customers\n"
                                     "2.check request reserve\n"
                                     "3.register request\n"
                                     "4.view store information\n"
                                     "5.edit store information\n"
                                     "6.search movie\n"
                                     "7.view rental information\n"
                                     "8.view list movie\n"))

        match select_operation:

            case 1:
                view_my_customers(staff_id)

            case 2:
                check_request_reserve(staff_id)

            case 3:
                register_request(staff_id)

            case 4:
                view_store_information(staff_id)

            case 5:
                edit_store_information(staff_id)

            case 6:
                search_movie()

            case 7:
                view_rental_information(staff_id, 1)

            case 8:
                view_list_movie()

            case 9:
                exit()

        print("-------------------------------------------------------------------")


if __name__ == '__main__':

    select_choice = int(input("Enter role (1.Manager, 2.Customer)"))

    match select_choice:

        case 1:
            signin_or_signup = int(input("1.signin"))
            staff_id = signin_manager()
            menu_manager(staff_id)

        case 2:
            signin_or_signup = int(input("1.signin, 2,signup"))

            match signin_or_signup:

                case 1:
                    customer_id = signin_customer()
                    menu_customer(customer_id)
                case 2:
                    customer_id = signup_customer()
                    menu_customer(customer_id)


cursor.close()