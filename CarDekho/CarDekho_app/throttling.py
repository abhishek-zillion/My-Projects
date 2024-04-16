from rest_framework.throttling import UserRateThrottle


class ReviewFullDetailThrottle(UserRateThrottle):
    scope = 'review_full_detail'


class ReviewDetailThrottle(UserRateThrottle):
    scope = 'review_detail'
