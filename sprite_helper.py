from math import sqrt


class FoundArea:
    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]

    def __repr__(self):
        return str(self.coordinates)

    @property
    def coordinates(self):
        return self.x, self.y

    def check(self, target):
        dx = (self.x - target[0])
        dy = self.y - target[1]
        d = sqrt(dx ** 2 + dy ** 2)
        # returns true if area is clear
        return d > 128

    def update(self, shift):
        self.x += shift.x
        self.y += shift.y


class EnemyUpdate:
    def __init__(self, ):
        return

    def update(self, obj, world_shift, player, tiles):
        if obj.id == "01":
            self.update_guardian(obj, world_shift, player, tiles)

    def update_guardian(self, obj, world_shift, player, tiles):
        """

        :param obj: Guardian instance to update
        :param world_shift: change in world space
        :param player: Player instance
        :param tiles: Tile group
        """
        obj.animate()
        obj.collision_objects = {"tiles": tiles, "enemies": player}

        # self.objself.combat(player)
        obj.rect.center += world_shift

        if obj.facing_right:
            if obj.facing_up:
                obj.head.center = (obj.rect.right - 16, obj.rect.top + 16)
            elif obj.facing_down:
                obj.head.center = (obj.rect.right - 16, obj.rect.bottom - 16)
            else:
                obj.head.center = (obj.rect.right - 16, obj.rect.centery)
        if obj.facing_left:
            if obj.facing_up:
                obj.head.center = (obj.rect.left + 16, obj.rect.top + 16)
            elif obj.facing_down:
                obj.head.center = (obj.rect.left + 16, obj.rect.bottom - 16)
            else:
                obj.head.center = (obj.rect.left + 16, obj.rect.centery)
        if obj.facing_up and not (obj.facing_left or obj.facing_right):
            obj.head.center = (obj.rect.centerx, obj.rect.top + 16)
        if obj.facing_down and not (obj.facing_left or obj.facing_right):
            obj.head.center = (obj.rect.centerx, obj.rect.bottom - 16)

        obj.target = (obj.target[0] + world_shift[0], obj.target[1] + world_shift[1])
        obj.range.center += world_shift
        obj.head.center += world_shift
        for area in obj.last_found_areas:
            area.update(world_shift)

        obj.generate_movement(player)
