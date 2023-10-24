from datetime import datetime
from django.db import connection
from rest_framework import status
from django.utils import timezone
from core.decorators import is_authenticated
from rest_framework.response import Response
from restaurant.serializers import RestaurantSerializer, MenuSerializer, MenuVoteSerializer
from restaurant.models import RestaurantModel, MenuModel, MenuVoteModel
from rest_framework.decorators import api_view


@api_view(["GET", "POST"])
@is_authenticated(['admin'])
def restaurant(request):
    if request.method == 'POST':
        serializer = RestaurantSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successfully created restaurant", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors, "data": None}, status=status.HTTP_400_BAD_REQUEST)
    else:
        restaurants = RestaurantModel.objects.all()

        serializer = RestaurantSerializer(restaurants, many=True)

        return Response({"message": "Successfully listed all restaurant", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@is_authenticated(['admin'])
def menu(request):
    if request.method == 'POST':
        current_datetime = timezone.now()

        menu_exists = MenuModel.objects.filter(restaurant__id=request.data.get(
            'restaurant'), created_at=current_datetime.date())

        if len(menu_exists) != 0:
            return Response({"message": 'Given restaurant, menu already exist for current day', "data": None}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MenuSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Successfully created menu", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors, "data": None}, status=status.HTTP_400_BAD_REQUEST)
    else:
        menus = MenuModel.objects.all()

        serializer = MenuSerializer(menus, many=True)

        return Response({"message": "Successfully listed all menus", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@is_authenticated(['employee'])
def menu_vote(request):

    vote_exist = MenuVoteModel.objects.filter(
        menu__id=request.data.get("menu"), user__id=request.user.get("id"))

    if len(vote_exist) != 0:
        return Response({"message": "You have already voted for this menu", "data": None}, status=status.HTTP_403_FORBIDDEN)

    serializer = MenuVoteSerializer(
        data={"menu": request.data.get('menu'), "user": request.user.get('id')})

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Successfully voted for menu", "data": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": serializer.errors, "data": None}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@is_authenticated(['employee'])
def menu_today(request):
    current_datetime = timezone.now()

    menus = MenuModel.objects.filter(created_at=current_datetime.date())

    serializer = MenuSerializer(menus, many=True)

    return Response({"message": "Successfully listed today's menus", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@is_authenticated()
def vote_result(request):
    date_string = request.GET.get("date")

    raw_query = """
        select 
            menu.id as menu_id, 
            menu.name as menu_name, 
            (select count(*) from menu_vote where menu_id=menu.id) as votes,
            restaurant.id as restaurant_id, 
            restaurant.name as restaurant_name 
        from 
            menu
        inner join restaurant
            on restaurant.id = menu.restaurant_id 
        where 
            menu.created_at='{}'        
        order by 
            votes desc;
        """.format(date_string)

    with connection.cursor() as cursor:
        cursor.execute(raw_query)
        results = cursor.fetchall()

    response = []

    for row in results:
        menu_id, menu_name, votes, restaurant_id, restaurant_name = row

        response.append({
            "menu_id": menu_id,
            "menu_name": menu_name,
            "votes": votes,
            "restaurant_id": restaurant_id,
            "restaurant_name": restaurant_name
        })

    return Response({"message": "Successfully generated vote result for today", "data": response}, status=status.HTTP_200_OK)
