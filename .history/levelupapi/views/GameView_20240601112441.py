from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, Game_Type


class GameView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        gamer = Gamer.objects.filter(uid=request.user.id).first()
        if gamer is None:
        # Return a response indicating that the gamer was not found
            return Response({'message': 'Gamer not found.'}, status=status.HTTP_404_NOT_FOUND)
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def list(self, request, format=None):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        games = Game.objects.all()
        game_type = request.query_params.get("type", None)
        if game_type is not None:
            games = games.filter(game_type__id=game_type)
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
        
    def create(self, request):
        """Handle POST operations
    
        Returns:
            Response -- JSON serialized game instance
        """
        print(request.user.id)
        gamer = Gamer.objects.filter(uid=request.user.id).first()
        if gamer is None:
        # Return a response indicating that the gamer was not found
            return Response({'message': 'Gamer not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Get the game type from the request data
        game_type_id = request.data["gameType"]
    
        # Get the Game_Type object with the provided id
        game_type = Game_Type.objects.filter(pk=game_type_id).first()
    
        # Check if game_type is None
        if game_type is None:
            # Return a response indicating that the game type was not found
            return Response({'message': 'Game type not found.'}, status=status.HTTP_404_NOT_FOUND)
    
        game = Game.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            number_of_players=request.data["numberOfPlayers"],
            skill_level=request.data["skillLevel"],
            game_type=game_type,
            gamer=gamer
        )
        serializer = GameSerializer(game)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
        Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.skill_level = request.data["skillLevel"]

        game_type = Game_Type.objects.get(pk=request.data["gameType"])
        game.game_type = game_type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Game
        fields = ('id', 'game_type', 'title', 'maker', 'number_of_players', 'skill_level')
