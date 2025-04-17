from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Questions

@api_view(['GET'])
def index(request):
    return Response({
        "message": "Hello, this is a JSON response!",
        "status": "success"
    }, status=status.HTTP_200_OK)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Questions

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Questions

@api_view(['POST'])
def save_questions(request):
    try:
        incoming_data = request.data

        if not isinstance(incoming_data, list):
            return Response({'error': 'Data must be a list of question objects'}, status=status.HTTP_400_BAD_REQUEST)

        # Group incoming questions by 'subject' (which maps to 'topic' in model)
        topic_map = {}
        for item in incoming_data:
            topic = item.get('subject')  # still expecting 'subject' in input
            if not topic:
                continue
            topic_map.setdefault(topic, []).append(item)

        # Process each topic
        for topic, questions in topic_map.items():
            obj = Questions.objects.filter(topic=topic).first()

            if obj:
                existing_qs = obj.questions or []
                existing_questions_set = {q['question'] for q in existing_qs}

                new_questions = [
                    q for q in questions if q['question'] not in existing_questions_set
                ]

                if new_questions:
                    obj.questions += new_questions
                    obj.save()
            else:
                Questions.objects.create(topic=topic, questions=questions)

        return Response({'message': 'Questions processed successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def get_topics(request):
    topics = Questions.objects.values_list('topic', flat=True)
    return Response({"topics": list(topics), "status": "success"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_questions(request, topic):
    try:
        question = Questions.objects.get(topic=topic)
        return Response({"questions": question.questions, "status": "success"}, status=status.HTTP_200_OK)
    except Questions.DoesNotExist:
        return Response({"error": "Topic not found"}, status=status.HTTP_404_NOT_FOUND)
