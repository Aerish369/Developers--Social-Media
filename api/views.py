from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from projects.models import Project, Review
from . serializers import ProjectSerializer


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET': '/api/projects/'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},

        {'PUT': '/api/projects/id/update-vote'},

        {'DELETE': 'api/projects/id/delete-vote'},

    ]

    return Response(routes)

@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def voteProject(request, pk):
    project = Project.objects.get(id = pk)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner = user,
        project = project,
    )
    review.value = data['value']
    review.save()
    project.getVoteCount

    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateVoteProject(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    review = Review.objects.get(owner=user, project=project)
    review.value = data['value']
    review.save()
    project.getVoteCount
    
    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteVoteProject(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile

    try:
        review = Review.objects.get(owner=user, project=project)
    except Review.DoesNotExist:
        print('Review does not exist')
        return Response('Review does not exist')
    

    if review.owner.user == request.user:
        print(f"Id: {review.id} body: {review.body} value: {review.value} is deleted")
        review.delete()
    else:
        print("Deletion Failed")

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)