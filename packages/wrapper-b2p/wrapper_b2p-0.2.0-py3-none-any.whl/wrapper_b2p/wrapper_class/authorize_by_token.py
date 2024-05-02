from .purchase_by_token import PurchaseByToken


class AuthorizeByToken(PurchaseByToken):
    path_to_point_api = 'AuthorizeByToken'
