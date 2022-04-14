from atexit import register
from django import template
from django.urls import reverse_lazy
import datetime

register = template.Library()


@register.simple_tag(takes_context=True)
def getNavbar(context, active):
    try:
        user = context.get("user")
    except Exception as e:
        print(e)
    navbar = f"""
    <ul class="nav nav-tabs bg-light" style="width:100%">
       
        <li class="nav-item" >
            <a class="nav-link {setActive(active,1)}" aria-current="page" href="{reverse_lazy('index')}">View Taxes</a>
        </li>

        <li class="nav-item ">
            <a class="nav-link {setActive(active,2)}   { setDisabled(user,3) }" href="{reverse_lazy('createUser')}" >Add Users</a>
        </li>
        
        <li class="nav-item">
            <a class="nav-link {setActive(active,3)}   { setDisabled(user,3) }" href="{reverse_lazy('viewUsers')}" >View Users</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="{reverse_lazy('logout')}" style="right:20px;position:absolute">Logout</a>
        </li>
    </ul>
    """

    return navbar


def setDisabled(user, min, only=False):

    if (user.user_type < min) if not only else (user.user_type == min):
        return "disabled"
    else:
        return ""


def setActive(original, this):
    if original == this:
        return "active"
    else:
        return ""


@register.simple_tag()
def getStatus(due):
    import pytz

    now = datetime.datetime.now(tz=pytz.timezone("Asia/Kolkata"))
    due = (due - now).days

    return "NEW" if due > 0 else "DELAYED"
