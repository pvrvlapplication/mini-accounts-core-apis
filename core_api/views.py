# accounts/views.py

from rest_framework.permissions import IsAuthenticated
from .models import Branch, Company, User
from .serializers import BranchSerializer, CompanySerializer, UserSerializer
from rest_framework import viewsets

# class CompanyView(APIView):

#     #permission_classes([IsAuthenticated])

#     def get(self, request, id=''):
#         if id:
#             result = Company.objects.get(id=id)
#             serializers = CompanySerializer(result)
#             return Response({'success': 'success', "students":serializers.data}, status=200)
#         result = Company.objects.all()
#         serializers = CompanySerializer(result, many=True)
#         return Response({'status': 'success', "students":serializers.data}, status=200)

#     def post(self, request):
#         serializer = CompanySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, id):
#         company_obj = Company.objects.get(id=id)
#         serializer = CompanySerializer(company_obj, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, id):
#         comp_obj = get_object_or_404(Company, pk=id)
#         if comp_obj:
#             comp_obj.delete()
#             return Response({"status": "success", "data": f"{comp_obj.name} Deleted Successfully."}, status=status.HTTP_200_OK)
#         else:
#             return Response({"status": "error", "data": f"{id} Not Found."}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and Branch user instances.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class CompanyViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Company instances.
    """

    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class BranchViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and Branch user instances.
    """

    serializer_class = BranchSerializer
    queryset = Branch.objects.all()
