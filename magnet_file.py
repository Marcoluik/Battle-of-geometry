import math


def move_items_towards_player(items, player, move_speed=4, attraction_radius=150):
    for item in items:
        dx, dy = player.x - item.x, player.y - item.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance < attraction_radius:
            if distance < attraction_radius/2:
                #Normalize the direction
                dx, dy = dx / distance, dy / distance
                # Move the item towards the player
                item.x += dx * move_speed * 2
                item.y += dy * move_speed * 2

            else:
                # Normalize the direction
                dx, dy = dx / distance, dy / distance
                # Move the item towards the player
                item.x += dx * move_speed
                item.y += dy * move_speed