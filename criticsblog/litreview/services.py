from litreview.models import Ticket, Review
from authentication.models import UserFollow




def get_users_viewable_tickets(user):
    """
    Tickets visibles :
    - ceux du request.user
    - ceux des utilisateurs suivis
    """

    followed_users = UserFollow.objects.filter(
        user=user
    ).values_list('followed_user', flat=True)

    allowed_users = list(followed_users) + [user.id]
    return Ticket.objects.filter(user_id__in=allowed_users)


def get_users_viewable_reviews(user):
    """
    Reviews visibles :
    - celles du request.user
    - celles des utilisateurs suivis
    """

    followed_users = UserFollow.objects.filter(
        user=user
    ).values_list('followed_user', flat=True)

    allowed_users = list(followed_users) + [user.id]

    return Review.objects.filter(
        user_id__in=allowed_users
    )
