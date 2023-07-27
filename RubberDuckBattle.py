import sys
import random
import inquirer


name = ""

#### NOTES ####
# 1. attack, attack_reduced do not need to be separate functions, try passing in a damage multiplier variable
# 2. change if self.health_potions > 1: to if self.health_potions >= 1: in heal function. the > and = if statements are doing the same thing
# 3. also in heal, if self.health_potions == 0: should be elif (saves time)
# 4. in the boost functions, if self.attack_potions == 0: and if self.defense_potions == 0: should also be elif
# 5. if attack and attack_reduced are combined, then normal_retaliate, and reduced_retaliate can also be combined
# 6. all of the if action["setting"] checks in main can use elif to save time

#Randomize damage output
def damage():
    dmg = random.randint(1, 20)
    return dmg


class Character(object):
    def __init__(self, name, hp, dmg, health_potions=8, attack_potions=4, defense_potions=4):
        self.name = name
        self.hp = hp
        self.dmg = dmg
        self.health_potions = health_potions
        self.attack_potions = attack_potions
        self.defense_potions = defense_potions
    #Check if either character is alive
    def alive(self):
        return self.hp > 0
    #Functions for attacking
    def attack(self, opponent):
        self.dmg = damage()
        opponent.hp = opponent.hp - self.dmg
    def attack_reduced(self, opponent):
        self.dmg = damage()
        self.dmg = self.dmg * 0.75
        opponent.hp = opponent.hp - self.dmg
    def attack_boost(self, opponent):
        self.dmg = damage()
        self.attack_potions = self.attack_potions -1
        if self.attack_potions >= 1:
            self.dmg = self.dmg * 1.25
            print("\nYou feel invigorated!")
            opponent.hp = opponent.hp - self.dmg
        if self.attack_potions == 0:
            print(
                "\nYou feel invigorated!"
                "\nYou are out of attack potions!"
                  )
            opponent.hp = opponent.hp - self.dmg
        if self.attack_potions < 0:
            self.attack_potions = 0
    def defense_boost(self):
        self.dmg = damage()
        self.defense_potions = self.defense_potions -1
        if self.defense_potions >= 1:
            print("\nYou feel reinforced!")
        if self.defense_potions == 0:
            print(
                "\nYou feel reinforced!"
                "\nYou are out of defense potions!"
                )
        if self.defense_potions < 0:
            self.defense_potions = 0
    #Function for self-healing
    def heal(self, player):
        self.health_potions = self.health_potions - 1
        if self.health_potions > 1:
            player.hp = player.hp + 25
            if player.hp > 100:
                player.hp = 100
            print(f"\nYour health is now {player.hp}.")
        if self.health_potions == 1:
            player.hp = player.hp + 25
            if player.hp > 100:
                player.hp = 100
            print(f"\nYour health is now {player.hp}.")
        if self.health_potions == 0:
            print(
                f"""\nYour health is now {player.hp}.
                \nYou are out of health potions!"""
                )
        if self.health_potions < 0:
            self.health_potions = 0


#Get the player's name
def get_name():
    global name
    try:
        name = input("\nWhat is your name? ")
        while name == '':
            TypeError(print("\nInvalid name"))
            name = input("What is your name? ")
    finally:
        return name


player = Character(get_name(), 100, int(damage()))
enemy = Character("Giant rubber duck", 150, int(damage()))


#Function for the enemy to attack
def normal_retaliate():
    if enemy.alive():
        enemy.attack(player)
        print(f"\n{enemy.name} attacked {player.name} for {enemy.dmg} damage.")
        if player.alive() == False:
            print(f"\n{player.name} died.")
            sys.exit()
    else:
        print(f"\n{player.name} killed {enemy.name}.")
        sys.exit()

def reduced_retaliate():
    if enemy.alive():
        enemy.attack_reduced(player)
        print(f"\n{enemy.name} attacked {player.name} for {enemy.dmg} damage.")
        if player.alive() == False:
            print(f"\n{player.name} died.")
            sys.exit()
    else:
        print(f"\n{player.name} killed {enemy.name}.")
        sys.exit()


#Main function, allows player to attack enemy or self-heal.
def main(player, enemy):
    fighting = True
    while fighting:
        while player.alive and enemy.alive:
            if player.hp < 100:
                print (f"\n{player.name}'s health: {player.hp}")
                print (f"{enemy.name}'s health: {enemy.hp}")
                list_of_actions = [
                    inquirer.List('setting',
                                  message="Choose action",
                                  choices=['attack', f'attack boost ({player.attack_potions})', f'defense boost ({player.defense_potions})', f'heal ({player.health_potions})'],
                                  ),
                ]
                action = inquirer.prompt(list_of_actions)
                if action["setting"] == f'heal ({player.health_potions})':
                    if player.health_potions == 0:
                        print("You are out of health potions!")
                        continue
                    else:
                        player.heal(player)
                        normal_retaliate()
                if action["setting"] == 'attack':
                    player.attack(enemy)
                    print(f"\n{player.name} attacked {enemy.name} for {player.dmg} damage.")
                    normal_retaliate()
                if action["setting"] == f'attack boost ({player.attack_potions})':
                    if player.attack_potions == 0:
                        print("You are out of attack potions!\n")
                        continue
                    else:
                        player.attack_boost(enemy)
                        print(f"\n{player.name} attacked {enemy.name} for {player.dmg} damage.")
                        normal_retaliate()
                if action["setting"] == f'defense boost ({player.defense_potions})':
                    if player.defense_potions == 0:
                        print("You are out of defense potions!\n")
                        continue
                    else:
                        player.defense_boost()
                        player.attack(enemy)
                        print(f"\n{player.name} attacked {enemy.name} for {player.dmg} damage.")
                        reduced_retaliate()
            if player.hp >= 100:
                normal_retaliate()


if __name__ == "__main__":
    main(player, enemy)


"""
Features to add:
1. Have the enemy spawn healers at 50% hitpoints.
2. Healers will heal enemy for 5 hitpoints each of the enemy's turn.
3. Healers will not respawn unless the enemy reaches 100% hitpoints again.
"""
