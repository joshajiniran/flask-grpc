import grp
import random
from concurrent import futures

import grpc

import recommendation_pb2_grpc
from recommendation_pb2 import (BookCategory, BookRecommendation,
                                RecommendationResponse)

books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title='The Marine Falcon'),
        BookRecommendation(id=2, title='Murder on the Orient Express'),
        BookRecommendation(id=3, title='Harry Porter Reborn'),
    ],
    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(id=4, title='The Gasby'),
        BookRecommendation(id=5, title='The Dune Chronicles'),
        BookRecommendation(id=6, title='Ender\s Game'),
    ],
    BookCategory.SELF_DEVELOPMENT: [
        BookRecommendation(id=7, title='The 7 Habits of Highy Effective People'),
        BookRecommendation(id=8, title='How to Win Friends and Influence People'),
    ],
}

class RecommendationService(recommendation_pb2_grpc.RecommendationsServicer):
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")
            
        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(books_for_category, num_results)
        
        return RecommendationResponse(recommendations=books_to_recommend)
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    recommendation_pb2_grpc.add_RecommendationsServicer_to_server(RecommendationService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
    

if __name__ == "__main__":
    serve()
