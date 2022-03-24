import constants
from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point

class HandleCollisionsAction(Action):
    """
    An update action that handles interactions between the actors.
    
    The responsibility of HandleCollisionsAction is to handle the situation when the snake collides
    with the food, or the snake collides with its segments, or the game is over.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
    """

    def __init__(self):
        """Constructs a new HandleCollisionsAction."""
        self._is_game_over = False
        self._winner = 0
        self._timer = 0

    def execute(self, cast, script):
        """Executes the handle collisions action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            self._handle_tail_growing(cast)
            self._handle_segment_collision(cast)
            self._handle_game_over(cast)
            
    def _handle_tail_growing(self, cast):
        self._timer += 1
        if self._timer % 5 == 0:
            snake = cast.get_first_actor("snakes")
            snake2 = cast.get_first_actor("snakes2")
            snake.grow_tail(1)
            snake2.grow_tail(1)
    
    def _handle_segment_collision(self, cast):
        """Sets the game over flag if the snake collides with one of its segments.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        snake = cast.get_first_actor("snakes")
        snake2 = cast.get_first_actor("snakes2")
        head = snake.get_segments()[0]
        head2 = snake2.get_segments()[0]
        segments = snake.get_segments()[1:]
        segments2 = snake2.get_segments()[1:]
        score = cast.get_first_actor("scores")
        score2 = cast.get_first_actor("scores2")
        
        for segment in segments:
            if head2.get_position().equals(segment.get_position()):
                score.add_points()
                self._winner = 1
                self._is_game_over = True
                
        for segment2 in segments2:   
            if head.get_position().equals(segment2.get_position()):
                score2.add_points()
                self._winner = 2
                self._is_game_over = True             
        
    def _handle_game_over(self, cast):
        """Shows the 'game over' message and turns the snake and food white if the game is over.
        
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if self._is_game_over:
            snake = cast.get_first_actor("snakes")
            snake2 = cast.get_first_actor("snakes2")
            segments = snake.get_segments()
            segments2 = snake2.get_segments()

            x = int(constants.MAX_X / 2)
            y = int(constants.MAX_Y / 2)
            position = Point(x, y)

            message = Actor()
            
            if self._winner == 1:
                message.set_text("Game Over, Blue Snake Wins!")
            else:
                message.set_text("Game Over, Green Snake Wins!")

            message.set_position(position)
            cast.add_actor("messages", message)

            for segment in segments:
                segment.set_color(constants.WHITE)
            for segment2 in segments2:
                segment2.set_color(constants.WHITE)    