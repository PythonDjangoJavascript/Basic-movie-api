from rest_framework.throttling import UserRateThrottle


class UserReviewDetailThrottle(UserRateThrottle):
    """Allow user to send limited request to review detail endpoint"""
    scope = 'review-detail'


class WatchDetailThrottle(UserRateThrottle):
    """Allow user to send limited request to watchDetail api endpoint"""
    scope = 'watch-detail'
