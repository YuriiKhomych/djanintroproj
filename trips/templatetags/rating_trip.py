from django import template

register = template.Library()

def rating(value):
    if value < 1:
        return "Quickly, join to us!"
    elif value > 5:
        return "You can choose place what you want"
    else:
        return "Hey! Go with us!"

register.filter('rating', rating)
