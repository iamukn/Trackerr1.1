from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from django.http import HttpResponseNotAllowed
from django.db import transaction
from shared.celery_tasks.tracking_info_tasks.verify_address_task import verify_shipping_address
from shared.celery_tasks.business_owners_task.upload_dp import upload_dp
from shared.aws_config.s3 import s3
from business.utils.resize_image import resize_image
from django.db.utils import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from user.serializers import UsersSerializer
from shared.logger import setUp_logger
from business.serializers import Business_ownerSerializer
from .business_owner_permission import IsBusinessOwner
from business.models import Business_owner
from user.models import User
from uuid import uuid4
from os import environ
from django.shortcuts import (get_object_or_404, get_list_or_404)
import botocore.exceptions
#from business.utils.resize_and_upload import resize_and_upload as upload_dp 

logger = setUp_logger(__name__, 'business.logs')

""" View that retrieves all business owners only when it's querried by
   a staff or an admin user 
"""

class GetAllBusinessOwners(APIView):
    """Views that returns all
    Business owners
    """

    permission_classes = [IsAdminUser,]
    
    @swagger_auto_schema(
        operation_description="Retrieves the information of all business users \nAdmin users only",
        operation_summary='Retrieve all business owners data',
        tags=["Business Owners"],
        responses={
            "200": openapi.Response(
                description='Business owners data retrieved successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description='ID of the user',
                            ),
                            'user': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'name': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description="name of the user"
                                        ),
                                    'email': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='email address'
                                        ),
                                    'phone_number': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='phone number'
                                        ),
                                    'is_verified': openapi.Schema(
                                        type=openapi.TYPE_BOOLEAN,
                                        description='specifies whether the user is verified'
                                        ),
                                    'account_type': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='specifies the account type of the user'
                                        ),
                                    'address': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='address of the user'
                                        ),
                                    'is_active': openapi.Schema(
                                        type=openapi.TYPE_BOOLEAN,
                                        description='specifies if a user is active'
                                        ),
                                    'updated_on': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='user data last update datetime if available, else null'
                                        ),
                                    'avatar':openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='link to the users avatar if available'
                                        )
                                    }
                                ),
                                'service': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description='service offered by user'
                                    ),
                                'business_name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description='business name of user'
                                    )
                            },
                example={
                    'id': 1,
                    'user': {
                        'name': 'john doe',
                        'email': 'johndoe@mail.com',
                        'phone_number': '080345676578',
                        'is_verified': True,
                        'account_type': 'business',
                        'address': '36 johndoe avenue example crescent, Canada',
                        'is_active': False,
                        'updated_on': None,
                        'avatar': ''
                        },
                    'service': 'parcel delivery',
                    'business_name': 'parcel 101'
                    },
                ),    
            ),
        ),

        },
    )
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
    """Views that handles the POST method on 
    Business owners
    """
    permission_classes = [AllowAny,]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def query_set(self,instance, id, *args, **kwargs):
        # Get the user object or return a 404    
        user = get_object_or_404(instance, pk=id)
        return user

    @swagger_auto_schema(
        operation_description="Registers a new user. If an avatar is included, the request should be "
            "in `multipart/form-data`. Otherwise, the request should be in JSON.",

        operation_summary='Create a new business owner',
        tags=['Business Owners'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='name of the user'
                    ),
                'phone_number': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='phone number of the user'
                    ),
                'email':openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='email address of the user'
                    ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='desired password of the user'
                    ),
                'address': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='address of the user'
                    ),
                'service': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='service offered by the user'
                    ),
                'business_name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='business name of the user'
                     ),
                'avatar': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_BINARY,
                    description='profile picture of the user'
                     ),
                'account_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='the account type'
                    )
                },
            required = ['name', 'email', 'phone_number', 'address', 'password', 'service', 'business_name', 'account_type'],
            example = {
                'name': "john doe",
                'email': "johndoe@example.com",
                "phone_number": "0709876567567",
                "address": "36 testing avenue, America",
                "password": "helloTh3r3",
                "service": "parcel delivery",
                "business_name": "johnny logistics",
                'account_type': 'business'
                }
            ),
        responses={
            "201": openapi.Response(
                description='user registered successfully',
                schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        description='Business owner ID of the user',
                    ),
                    'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="name of the user"
                        ),
                        'email': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='email address'
                        ),
                        'phone_number': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='phone number'
                        ),
                        'is_verified': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description='specifies whether the user is verified'
                        ),
                        'account_type': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='specifies the account type of the user'
                        ),
                        'address': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='address of the user'
                        ),
                        'is_active': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description='specifies if a user is active'
                        ),
                        'updated_on': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='user data last update datetime if available, else null'
                        ),
                        'avatar':openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='link to the users avatar if available'
                        )
                            }
                                ),
                    'service': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='service offered by user'
                    ),
                    'business_name': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='business name of user'
                    )
                        }
                            )
                    ),
            "400": openapi.Response(
                    description="Error: Bad Request",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'error': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Error message describing why the input is invalid'

                                )
                            },
                        example={
                            'error': 'account type must be business'
                            }
                        )
                    ),
            "404": openapi.Response(
                    description="Error: Address Not Found",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'error': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Error message describing the error'
                                )
                            },
                        example={
                            'error': 'address cannot be found on the map, enter a valid address'
                            }
                        )
                    )
                    }
                )
    
    def post(self,request, *args, **kwargs):
        # This will handle registration of business owners
         
        if not request.data.get('account_type') == 'business':
            logger.error('account_type is not business owner')
            return Response({"error":"account type must be business"}, status=status.HTTP_400_BAD_REQUEST)
        if 'address' not in request.data:
            return Response({'error': 'address is required'}, status=status.HTTP_400_BAD_REQUEST)

            #
        try:
            with transaction.atomic(): 
                # get the lat and lng for the business owner
                data = request.data
                avatar = data.get('avatar')

                if avatar:
                    data.pop('avatar')

                address = verify_shipping_address.apply_async(kwargs={'address': data.get('address', '').capitalize()})
                address = address.get(timeout=60)

                
                # handle errors from address field
                if 'error' in address:
                    return Response({'error': 'address cannot be found on the map, please enter a valid address'}, status=status.HTTP_404_NOT_FOUND)

                user = UsersSerializer(data=request.data, context={'request': request})
                
                new_uuid = uuid4()
                user_s3_key = ""
                if avatar:
                    content_type = str(avatar.content_type).split('/')[-1]
                    print(content_type)

                    if not content_type.lower() in ['jpg', 'jpeg', 'png']:
                        return Response({'error': "avatar must either be jpg, jpeg or png"}, status=status.HTTP_400_BAD_REQUEST)

                    user_s3_key = f"profile-pics/{new_uuid}.{content_type}"

                    
                business_data = {
                    'business_name': request.data.get('business_name'),
                    'service': request.data.get('service'),
                    'latitude': address.get('latitude'),
                    'longitude': address.get('longitude'),
                    'business_owner_uuid': str(new_uuid),
                    'profile_pic_key': user_s3_key
                        }
                business_owner = Business_ownerSerializer(data=business_data, context={'request': request})
            

                if not business_owner.is_valid() and not user.is_valid():
                    print(user.errors, business_owner.errors)
                    return Response((user.errors, business_owner.errors), status=status.HTTP_400_BAD_REQUEST)
            
                elif not business_owner.is_valid():
                    print(business_owner.errors)
                    return Response(business_owner.errors, status=status.HTTP_400_BAD_REQUEST)

                elif not user.is_valid():
                    return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
            
                elif business_owner.is_valid() and user.is_valid():
                    if avatar:
                        upload_dp.delay(avatar.read(),user_s3_key)
                        user.save(avatar=f"{environ.get('TRACKERR_CDN_URL')}/{user_s3_key}")
                        business_owner.save(user=self.query_set(User, user.instance.id))
                    else:
                        user.save()
                        business_owner.save(user=self.query_set(User, user.instance.id))
                    return Response(business_owner.data, status=status.HTTP_201_CREATED)
                return Response({'error': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as e:
            return Response(str(e.args[0].strip('\n')), status=status.HTTP_400_BAD_REQUEST)
        
        except botocore.exceptions.ClientError as e:
            error_message = e.response['Error'].get('Message', 'S3 upload failed.')
            return Response({"error": error_message}, status=500)

        except ValueError as e:
            logger.error(e)
            return Response(business_owner.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            raise e
            logger.error(e)
            return Response({'error': str(e)})

"""
  Class to retrieve, modify and delete a business_owner
"""

class Business_ownerRoute(APIView):
    """ 
    Method that returns information 
    about a single business user
    """
    def query_set(self,instance, id, *args, **kwargs):
        # Get the user object or return a 404
        user = get_object_or_404(instance, pk=id)
        # return user a 404
        return user

    permission_classes = [IsBusinessOwner,]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    def authorized(self, request, business_id):
        id = business_id
        user_id = request.user.business_owner.id
        return user_id == int(id)
    # swagger documentation
    @swagger_auto_schema(
        operation_summary="Retrieve information of a single user",
        operation_description="GET endpoint that retrieves information of a business owner",
        tags=['Business Owners'],
        responses = {
            "200": openapi.Response(
            description="GETs the information of a single user",
            schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description="Business owner ID",
                    ),
                "user": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "name":openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="name of user"
                        ),
                        "email":openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="email of user"
                        ),
                        "phone_number":openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="email of user"
                        ),
                        "is_verified":openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description="verification status of the user"
                        ),
                        "account_type":openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="account type of the user"
                        ),
                        "address":openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="user address"
                        ),
                        "is_active":openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description="active status of the user",
                        ),
                        "updated_on":openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="user profile update time",
                        ),
                        "avatar":openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="user profile update time",
                        ),
                        "service":openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="service offerred by user",
                        ),
                        "business_name":openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="service offerred by user",
                        ),
                        }
                    )
            
                }
            )
            ),
            "401": openapi.Response(
                description="Error: Unauthorized",
                schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Authentication credentials were not provided.")
                }
                )
                ),
            "403": openapi.Response(
                description="Error: Forbidden",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="forbidden")
                        }
                    )
                )
            }
                )
    # Get a business users data
    def get(self, request, id, *args, **kwargs):

        """ Returns information of a single
            Business owner
        """
        if not self.authorized(request, id):
            return Response({'error': 'forbidden'}, status=status.HTTP_403_FORBIDDEN)
        user = self.query_set(Business_owner, id)
        serializer = Business_ownerSerializer(user, context={'request': request})
        if user:
            data = serializer.data
            name = data.get('user').get('name')
            if name:
                name = name.split(' ')[0].capitalize()
                data['user']['name'] = name + '👌'
            data['user'].pop('created_on')
            data['user'].pop('updated_on')
            data['user'].pop('phone_number')
            print(data)
            return Response(data, status=status.HTTP_200_OK)
        return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Updates a business owners data",
        operation_summary="Business owners data update",
        tags=['Business Owners'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='business owners name'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='business owners email'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='business owners phone number'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='business owners address'),
                },
            example={
                'name': "Jane Doe",
                'email': "janedoe@example.com",
                'phone_number': '+234904567887',
                'address': '1245 example avenue, accra, Ghana'
                }
            ),
        responses={
            '206': openapi.Response(
                description='Updated Successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='users business ID'),
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'name':openapi.Schema(type=openapi.TYPE_STRING, description='users name'),
                                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='users phone number'),
                                'email': openapi.Schema(type=openapi.TYPE_STRING, description='users email'),
                                'address': openapi.Schema(type=openapi.TYPE_STRING, description='users address'),
                                'is_verified': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='verification status of user'),
                                'account_type': openapi.Schema(type=openapi.TYPE_STRING, description='users account type'),
                                'is_active': openapi.Schema(type=openapi.TYPE_STRING, description='status of the user'),
                                'updated_on': openapi.Schema(type=openapi.TYPE_STRING, description='users profile update time'),
                                'avatar': openapi.Schema(type=openapi.TYPE_STRING, description='users avatar url if available'),
                                }),
                        'service': openapi.Schema(type=openapi.TYPE_STRING, description='service offerred by user'),
                        'business_name': openapi.Schema(type=openapi.TYPE_STRING, description='business name'),
                        },
                    example={
                        'id': 1,
                        'user':{
                            'name': 'john doe',
                            'phone_number': '+234098765459',
                            'email': 'johndoe@example.com',
                            'address': '1234 example avenue, accra ghana',
                            'is_verified': True,
                            'is_active': True,
                            'account_type': 'business',
                            'updated_on': '2024-12-01T22:04:46.779558Z',
                            'avatar': 'https://trackerr.live/static/images/admin/johndoe.jpg',
                          },
                          'service': 'parcel delivery',
                          'business_name': 'johny drips'
                        }
                    )
                        ),
            '401': openapi.Response(
                description='Error: Unauthorized',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication credentials were not provided.'),
                        },
                    example={
                        'detail': 'Authentication credentials were not provided.'
                        }
                    )
                ),
            '403': openapi.Response(
                description='Error: Forbidden',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='forbidden'),
                           },
                    example={
                        'detail': 'forbidden'
                        }
                    )
                )
            }
        )
    # Update a business users data
    def put(self, request, id, *args, **kwargs):
        """
            Modifies the existing data of a single business user
        """
        if not self.authorized(request, id):
            return Response({'error': 'forbidded'}, status=status.HTTP_403_FORBIDDEN)
        business = self.query_set(Business_owner, id)
        user = business.user
        data = request.data
        if 'password' in data:
            data.pop('password')
        with transaction.atomic():
            user_serializer = UsersSerializer(user, data=data, partial=True)
            business_serializer = Business_ownerSerializer(business, data=data, context={'request': request}, partial=True)
                
            if user_serializer.is_valid() and business_serializer.is_valid():
                user_serializer.save()
                business_serializer.save()

                return Response(business_serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # swagger documentation for the patch route
    @swagger_auto_schema(
        operation_description='Update a business owners partial data',
        operation_summary='Partial data update',
        tags=['Business Owners'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='john doe'),
                'email':openapi.Schema(type=openapi.TYPE_STRING, description='johndoe@example.com'),
                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='+234098679867'),
                },
            example={
                'name':'john doe',
                'email': 'johndoe@example.com',
                'phone_number':'+234098679867'
                }
            ),
        responses = {
            '206': openapi.Response(
                description='Partial Update Successful',
                schema = openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Users unique ID'),
                    'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "name":openapi.Schema(type=openapi.TYPE_STRING, description='Users name'),
                            "email":openapi.Schema(type=openapi.TYPE_STRING, description='Users email'),
                            "phone_number": openapi.Schema(type=openapi.TYPE_STRING, description='Users phone number'),
                            'is_verified': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='verification status'),
                            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='active status'),
                            'address': openapi.Schema(type=openapi.TYPE_STRING, description='Users address'),
                            'account_type': openapi.Schema(type=openapi.TYPE_STRING, description='account type'),
                            "updated_on": openapi.Schema(type=openapi.TYPE_STRING, description='profile last update time'),
                            'avatar': openapi.Schema(type=openapi.TYPE_STRING, description='avatar url if available'),
                            }
                        ),
                    'service': openapi.Schema(type=openapi.TYPE_STRING, description='service offerred'),
                    'business_name': openapi.Schema(type=openapi.TYPE_STRING, description='Business name'),
                    }
                ,
                example={
                    "id": 1,
                     "user": {
                          "name": "jixy doe",
                          "email": "testuser@gmail.com",
                          "phone_number": "+234098679867",
                          "is_verified": True,
                          "account_type": "business",
                          "address": "1245 example avenue, accra, ghana",
                          "is_active": True,
                          "updated_on": "2024-12-01T23:04:49.301895Z",
                          "avatar": ""
                        },
                    "service": "parcel delivery",
                    "business_name": "volta"
                }
                ),
                ),

            '401': openapi.Response(
                description='Error: Unauthorized',
                schema = openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_INTEGER, description='Authentication credentials were not provided.')
                        },
                example={
                    'detail': 'Authentication credentials were not provided.'
                    }
                )
            ),

            '403': openapi.Response(
                description='Error: Forbidden',
                schema = openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_INTEGER, description='forbidden')
                        },
                    example={
                        'error': 'forbidden'
                        }
                    )
                ),
            }
            )
    def patch(self, request, id, *args, **kwargs):
        """
           modifies existing data of a single user using 
           patch request
        """
        if not self.authorized(request, id):
            return Response({'error': 'forbidded'}, status=status.HTTP_403_FORBIDDEN)

        business = self.query_set(Business_owner, id)
        user = business.user

        data = request.data
        if 'password' in data:
            data.pop('password')

        with transaction.atomic():
            user_ser = UsersSerializer(user, data=data, partial=True)
            business_ser = Business_ownerSerializer(business, data=data, context={'request': request}, partial=True)
        
            if user_ser.is_valid() and business_ser.is_valid():
                user_ser.save()
                business_ser.save()
                return Response(business_ser.data, status=status.HTTP_206_PARTIAL_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # Swagger Documentation 
    @swagger_auto_schema(
        operation_summary='Delete a business owner',
        operation_description='DELETE endpoint for deleting a business users account',
        tags=['Business Owners'],
        responses={
            '401': openapi.Response(
                description='Error Unauthorized',
                schema=openapi.Schema(
                  type=openapi.TYPE_OBJECT,
                  properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Given token not valid for any token type'),
                    'code': openapi.Schema(type=openapi.TYPE_STRING, description='token_not_valid'),
                    'message': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "token_class": openapi.Schema(type=openapi.TYPE_STRING, description='AccessToken'),
                                "token_type": openapi.Schema(type=openapi.TYPE_STRING, description='access'),
                                 "message": openapi.Schema(type=openapi.TYPE_STRING, description="Token is invalid or expired")
                                }
                            ),
                        ),
                      },
                  example={
                    "detail": "Given token not valid for any token type",
                    "code": "token_not_valid",
                    "messages": [
                            {
                            "token_class": "AccessToken",
                            "token_type": "access",
                            "message": "Token is invalid or expired"
                            }
                        ]
                      }
                    )

                ),
            '403': openapi.Response(
                description='Error: Forbidden',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, description='forbidden')
                        },
                    example={
                        'error': 'forbidden'
                        }
                    ),
                ),

            '204': openapi.Response(
                description='Success: Account Deleted! \n No content is returned!',
                ),

            }
            )
    def delete(self, request,id, *args, **kwargs):
        if not self.authorized(request, id):
            return Response({'error': 'forbidded'}, status=status.HTTP_403_FORBIDDEN)
        if request.user:
            id=request.user.id
            try:
                user = User.objects.get(id=id)

                user.delete()
            
                return Response({"status": "successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

            except User.DoesNotExist:
                return Response({"status":"user not found"}, status=status.HTTP_404_NOT_FOUND)    

        return Response({"status":"user not found"}, status=status.HTTP_404_NOT_FOUND)
