from menu import Menu, MenuItem
from django.core.urlresolvers import reverse




# Define children for the my account menu
myaccount_children = (
    MenuItem("Edit Profile",
             reverse("profile"),
             weight=10),
    MenuItem("Admin",
             reverse("admin:index"),
             weight=80,
             separator=True,
             check=lambda request: request.user.is_superuser),
    MenuItem("Logout",
             reverse("logout"),
             weight=90,
             separator=True),
)

# Add a My Account item to our user menu
Menu.add_item("user", MenuItem("My Account",
                               reverse("logout"),
                               weight=15,
                               children=myaccount_children))

