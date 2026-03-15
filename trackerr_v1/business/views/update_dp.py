from django.shortcuts import render
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from business.views.business_owner_permission import IsBusinessOwner
from user.serializers import UsersSerializer
from business.models import Business_owner
from user.models import User
from business.serializers import Business_ownerSerializer
from shared.celery_tasks.business_owners_task.upload_dp import upload_dp 
from os import environ
from uuid import uuid4


"""
Views for the user application
"""

class UpdateDp(APIView):
    ''' Method to update business owners avatar
    '''
    # swagger documentation
    @swagger_auto_schema(
        operation_summary='Partial Update Profile picture of a business owner',
        operation_description='Partially update profile picture by sending either jpeg, jpg or png to the endpoint as a multipart form data content type',
        tags=['Business Owners'],
        responses={
            '200': openapi.Response(
                description='Successful',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'msg':openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={'avatar': openapi.Schema(type=openapi.TYPE_STRING,description='Profile picture URL')}
                            )
                        },
                    example = {
                        'msg': {"avatar": "https://example.com/profile-pics/fgh-fghjk-ghj.jpeg"}
                    }
                    ),
                ),
            '401': openapi.Response(
                description='Error: Unauthorized',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error message'),
                        },
                    example={
                        'detail': "Authentication credentials were not provided."
                        }
                    )
                ),
            '403': openapi.Response(
                description='Error: Forbidden',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error message'),
                        },
                    example={
                        'detail': 'You do not have permission to perform this action.'
                        }
                    ),
                ),
            '404': openapi.Response(
                description='Error: Not Found',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error message'),
                         },
                    example={
                        'detail': "user does not exist"
                         }
                    ),
                ),
            '400': openapi.Response(
                    description="Bad Request",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='error message'),
                        },
                    example={
                        'error': 'invalid file format'
                        }
                        )
                    )
            }
            )
    def patch(self, request, id,  *args, **kwargs):
        try:
            with transaction.atomic():
                #user = request.user
                #business_owner_obj = request.user.business_owner
                print('Atomic run')
                user = User.objects.select_for_update().get(id=request.user.id)
                business_owner_obj = user.business_owner

                if not int(business_owner_obj.id) == int(id):
                    return Response({'error': 'forbidden'}, status.HTTP_400_BAD_REQUEST)
                uuid = business_owner_obj.business_owner_uuid
                #return Response('0')
                avatar = request.data.get('avatar')
                uploaded_file_type = ""
                CDN_URL = environ.get('TRACKERR_CDN_URL')

                if avatar:
                    uploaded_file_type = avatar.content_type.split('/')[-1]
                    if not uploaded_file_type.lower() in ['jpeg', 'png', 'jpg']:
                        return Response({'error': 'invalid file format'}, status=status.HTTP_400_BAD_REQUEST)
                
                # check if there's a profile pic key
                if uuid:
                    # update the photo in aws
                    if not uploaded_file_type in ['jpeg', 'png', 'jpg']:
                        return Response({'error': 'invalid file format'}, status=status.HTTP_400_BAD_REQUEST)
                    key = f"{uuid}.{uploaded_file_type}"
                    upload_dp.delay(file_obj=avatar.read(), key=key)
                     
                    business_serializer = Business_ownerSerializer(business_owner_obj, data={'profile_pic_key': key}, partial=True)
                    user_serializer = UsersSerializer(user, data={'avatar': f'{CDN_URL}/{key}'}, partial=True)
                    if business_serializer.is_valid() and user_serializer.is_valid():
                        business_serializer.save()
                        user_serializer.save()
                    else:
                        return Response({'error': business_serializer.errors if business_serializer.errors else user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({'msg': {'avatar':f'{CDN_URL}/{key}'}}, status=status.HTTP_200_OK)
                # no key? create key, store in db and upload to aws
                new_uuid = str(uuid4())
                key = "profile-pics/{}.{}".format(new_uuid, uploaded_file_type)
                avatar_url = f'{CDN_URL}/{key}'
                # update the instance in the dp
                business_serializer = Business_ownerSerializer(business_owner_obj, data={'profile_pic_key': key, 'business_owner_uuid': new_uuid}, partial=True, context={'request': {'profile_pic_key': key, 'business_owner_uuid': new_uuid}})
                user_serializer = UsersSerializer(user, data={'avatar': avatar_url}, partial=True)
                if business_serializer.is_valid() and user_serializer.is_valid():
                    # update and save instance
                    upload_dp.delay(file_obj=avatar.read(), key=key)
                    business_serializer.save()
                    print(business_serializer.data)
                    user_serializer.save()
                    return Response({'msg': {'avatar':avatar_url}}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': business_serializer.errors if business_serializer.errors else user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Business_owner.DoesNotExist:
            return Response({'error': 'cannot update because user does not exist!'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'cannot update because user does not exist!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise(e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
