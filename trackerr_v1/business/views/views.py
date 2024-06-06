from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from django.db import transaction
from user.serializers import UsersSerializer
from shared.logger import setUp_logger
from business.serializers import Business_ownerSerializer
from .business_owner_permission import IsBusinessOwner
from business.models import Business_owner
from user.models import User
from django.shortcuts import (get_object_or_404, get_list_or_404)



logger = setUp_logger(__name__, 'business.logs')

""" View that retrieves all business owners only when it's querried by
   a staff or an admin user 
"""

class GetAllBusinessOwners(APIView):
    """Views that returns all
    Business owners
    """

    permission_classes = [IsAdminUser,]
    

    def get(self, request, *args, **kwargs):

        # This will return all Business owners information
        # That exist in the database
        # Fetch business owners model from the database
        # Serializer it and return a json response
        business_owner = get_list_or_404(Business_owner)
        business_owner_serializer = Business_ownerSerializer(business_owner, many=True)
        return Response(business_owner_serializer.data, status=status.HTTP_200_OK)

""" 
  Views to handle http methods on for Business owner
"""

class Business_ownerRegistration(APIView):
    """Views that handles the GET and POST method on 
    Business owners
    """
    permission_classes = [AllowAny,]
    parser_classes = [JSONParser,]

    def query_set(self,instance, id, *args, **kwargs):
        # Get the user object or return a 404    
        user = get_object_or_404(instance, pk=id)
        return user


    def post(self,request, *args, **kwargs):
        # This will handle registration of business owners
         
        if not request.data.get('account_type') == 'business':
            logger.error('account_type is not business owner')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic(): 
        
                user = UsersSerializer(data=request.data)

                business_owner = Business_ownerSerializer(data={'business_name': request.data.get('business_name'), 'service': request.data.get('service'),})
            

                if not business_owner.is_valid() and not user.is_valid():
                    return Response((user.errors, business_owner.errors), status=status.HTTP_400_BAD_REQUEST)
            
                elif not business_owner.is_valid():
                    return Response(business_owner.errors, status=status.HTTP_400_BAD_REQUEST)

                elif not user.is_valid():
                    return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
            
                elif business_owner.is_valid() and user.is_valid():
                
                    user.save()
                    business_owner.save(user=self.query_set(User, user.instance.id))
                    return Response(business_owner.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            logger.error(e)
            return Response(business_owner.errors, status=status.HTTP_400_BAD_REQUEST)


"""
  Class to retrieve, modify and delete a business_owner
"""

class Business_ownerRoute(Business_ownerRegistration):
    """ 
    Method that returns information 
    about a single business user
    """
    permission_classes = [IsBusinessOwner,]

    def get(self, request, id, *args, **kwargs):

        """ Returns information of a single
            Business owner
        """
        
        user = self.query_set(Business_owner, id)
        serializer = Business_ownerSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        """
            Modifies the existing data of a single business user
        """

        business = self.query_set(Business_owner, id)
        user = business.user
        
        try:
            user_data = request.data.pop('user')
            password = user_data.pop('password')
        except Exception:
            return Response('all user profile data is required!', status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            user_serializer = UsersSerializer(user, data=user_data, partial=True)

            business_serializer = Business_ownerSerializer(business, data=request.data, partial=True)
                
            if user_serializer.is_valid() and business_serializer.is_valid():
 
                user_serializer.save()
                user_serializer.instance.set_password(password)
                user_serializer.save()
                business_serializer.save()

                return Response(business_serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self, request, id, *args, **kwargs):
        """
           modifies existing data of a single user using 
           patch request
        """

        business = self.query_set(Business_owner, id)
        user = business.user

        
        if 'user' in request.data:
            user_data = request.data.pop('user')

            with transaction.atomic():
                user_ser = UsersSerializer(user, data=user_data, partial=True)
                business_ser = Business_ownerSerializer(business, data=request.data, partial=True)
        
                if user_ser.is_valid() and business_ser.is_valid():
                    user_ser.save()
                    business_ser.save()
            
                    return Response(business_ser.data, status=status.HTTP_206_PARTIAL_CONTENT)

        with transaction.atomic():
            business_ser = Business_ownerSerializer(business, data=request.data, partial=True)
            if business_ser.is_valid():
                business_ser.save()
                return Response(business_ser.data, status=status.HTTP_206_PARTIAL_CONTENT)

            return Response(status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request,id, *args, **kwargs):

        if request.user:
            id=request.user.id
            try:
                user = User.objects.get(id=id)

                user.delete()
            
                return Response({"status": "successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

            except User.DoesNotExist:
                return Response({"status":"User not found"}, status=status.HTTP_404_NOT_FOUND)    

        return Response({"status":"User not found"}, status=status.HTTP_404_NOT_FOUND)
