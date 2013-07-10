from menu import Menu, MenuItem
from django.core.urlresolvers import reverse


# Add two items to our main menu
Menu.add_item("main", MenuItem("Contestants",
                               reverse("contestants"),
                               weight=10))

Menu.add_item("main", MenuItem("Contests",
                               reverse("contests"),
                               weight=20))

Menu.add_item("main", MenuItem("Scores",
                               reverse("scores"),
                               weight=30))



# # # Define children for the my account menu
# # myaccount_children = (
# #     MenuItem("Edit Profile",
# #              reverse("accounts.views.editprofile"),
# #              weight=10,
# #              icon="user"),
# #     MenuItem("Admin",
# #              reverse("admin:index"),
# #              weight=80,
# #              separator=True,
# #              check=lambda request: request.user.is_superuser),
# #     MenuItem("Logout",
# #              reverse("accounts.views.logout"),
# #              weight=90,
# #              separator=True,
# #              icon="user"),
# # )

# # # Add a My Account item to our user menu
# # Menu.add_item("user", MenuItem("My Account",
# #                                reverse("accounts.views.myaccount"),
# #                                weight=10,
# #                                children=myaccount_children))

