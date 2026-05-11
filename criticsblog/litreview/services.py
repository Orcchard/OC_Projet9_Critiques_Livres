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
    # user=user: Je cherche les objets UserFollow dont le champ user est égal à la variable user

    allowed_users = list(followed_users) + [user.id]
    return Ticket.objects.filter(
        user_id__in=allowed_users
    ).annotate(
        content_type=models.Value('TICKET', models.CharField()),
        has_review=Exists(
            Review.objects.filter(ticket_id=OuterRef('pk'))
        )
    ) # annotateajoute des champs calculés temporaires à chaque objet.
    # Ajouter à chaque Ticket : ticket.has_review, tickets avec review
    # OuterRef('pk') le ticket actuel de la requête principale

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

    return Review.objects.filter(user_id__in=allowed_users)
