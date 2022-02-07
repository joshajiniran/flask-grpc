from recommendation_pb2 import BookCategory, RecommendationRequest

from .recommendations import RecommendationService


def test_recommendation():
    service = RecommendationService()
    request = RecommendationRequest(user_id=1, category=BookCategory.SCIENCE_FICTION, max_results=1)
    response = service.Recommend(request, None)
    assert len(response.recommendations) == 1
