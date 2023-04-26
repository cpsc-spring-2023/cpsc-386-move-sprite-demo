from itertools import cycle
from random import randint
import pygame
import assets
import rgbcolors

def load_sprite_sheet(filename, img_dim_x, img_dim_y, num_images, colorkey=None):
    # Limitation: only considers a 1D strip of images where the images
    # are tiled from left to right
    try:
        sheet = pygame.image.load(filename)
    except pygame.error as pygame_error:
        print('\n'.join(pygame_error.args))
        raise SystemExit(
            f'Unable to open "{filename}" {pygame.get_error()}'
        ) from pygame_error
    rects = [
        pygame.Rect(0 + (img_dim_x * n), 0, img_dim_x, img_dim_y)
        for n in range(num_images)
    ]
    images = []
    for r in rects:
        image = pygame.Surface(r.size)
        image.blit(sheet, (0, 0), r)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        images.append(image)
    return images
    # self._images = [pygame.Surface(x.size).blit(self._sheet, (0, 0), x) for x in r]

# Taken from the pygame examples
def load_image(filename, colorkey=None, scale=1):
    image = pygame.image.load(filename)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

class Circle:
    """Class representing a ball with a bounding rect."""

    min_speed = 0.25
    max_speed = 5.0

    def __init__(self, position, speed, radius, color, name="None"):
        self._position = position
        self._original_position = pygame.math.Vector2(position)
        assert speed <= Circle.max_speed
        assert speed >= Circle.min_speed
        self._speed = speed
        self._radius = radius
        self._color = color
        self._name = name

    @property
    def radius(self):
        """Return the circle's radius"""
        return self._radius

    @property
    def position(self):
        """Return the circle's position."""
        return self._position

    @property
    def original_position(self):
        return self._original_position

    @position.setter
    def position(self, val):
        """Set the circle's position."""
        self._position = val

    @property
    def speed(self):
        """Return the circle's speed."""
        return self._speed

    @property
    def inverse_speed(self):
        return Circle.max_speed - self._speed

    def move_ip(self, x, y):
        self._position = self._position + pygame.math.Vector2(x, y)

    @property
    def rect(self):
        """Return bounding rect."""
        left = self._position.x - self._radius
        top = self._position.y - self._radius
        width = 2 * self._radius
        return pygame.Rect(left, top, width, width)

    @property
    def width(self):
        """Return the width of the bounding box the circle is in."""
        return 2 * self._radius

    @property
    def height(self):
        """Return the height of the bounding box the circle is in."""
        return 2 * self._radius

    def contains(self, point, buffer=0):
        """Return true if point is in the circle + buffer"""
        v = point - self._position
        distance = v.length()
        # assume all circles have the same radius
        seperating_distance = 2 * (self._radius + buffer)
        return distance <= seperating_distance

    def draw(self, screen):
        """Draw the circle to screen."""
        pygame.draw.circle(screen, self._color, self.position, self.radius)

    def __repr__(self):
        """Circle stringify."""
        return f'Circle({repr(self._position)}, {self._radius}, {self._color}, "{self._name}")'


class CircleSprite(pygame.sprite.Sprite):
    min_speed = 0.25
    max_speed = 5.0

    def __init__(self, position, speed, name="None"):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(assets.get('circleimage'), -1)
        self._position = position
        self.rect.center = self._position
        self._original_position = pygame.math.Vector2(position)
        assert speed <= CircleSprite.max_speed
        assert speed >= CircleSprite.min_speed
        self._speed = speed
        self._radius = 5

    def update(self):
        self.rect.center = self._position

    @property
    def radius(self):
        """Return the circle's radius"""
        return self._radius

    @property
    def position(self):
        """Return the circle's position."""
        return self._position

    @property
    def original_position(self):
        return self._original_position

    @position.setter
    def position(self, val):
        """Set the circle's position."""
        self._position = val

    @property
    def speed(self):
        """Return the circle's speed."""
        return self._speed

    @property
    def inverse_speed(self):
        return CircleSprite.max_speed - self._speed

    def move_ip(self, x, y):
        self._position = self._position + pygame.math.Vector2(x, y)

    def draw(self, screen):
        """Draw the circle to screen."""
        pygame.draw.circle(screen, rgbcolors.red, self.position, self.radius)

    def contains(self, point, buffer=0):
        """Return true if point is in the circle + buffer"""
        v = point - self._position
        distance = v.length()
        # assume all circles have the same radius
        seperating_distance = 2 * (self._radius + buffer)
        return distance <= seperating_distance

class CircleSpriteSheet(CircleSprite):
    def __init__(self, position, speed, name, scene):
        # pygame.sprite.Sprite.__init__(self)
        super().__init__(position, speed, name)
        self._scene = scene
        self._elapsed_time = 0
        n = randint(1, 4)
        sheet_name = f'circlesheet{n}'
        self.images = load_sprite_sheet(assets.get(sheet_name), 192, 192, 5, -1)
        self._image_pool = cycle(self.images)
        self.image = next(self._image_pool)
        self._position = position
        self.rect.center = self._position
        self._original_position = pygame.math.Vector2(position)
        assert speed <= CircleSprite.max_speed
        assert speed >= CircleSprite.min_speed
        self._speed = speed
        self._radius = 5

    def update(self):
        self._elapsed_time += self._scene.delta_time
        if self._elapsed_time > 75:
            self.image = next(self._image_pool)
            self._elapsed_time = 0
        self.rect.center = self._position

