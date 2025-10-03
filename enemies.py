from mechanics import *
from random import *



def generate_enemy(enemy):
    #Names to randomly pick from
    names = ["Bob", "Michael", "Peter", "John", "Harold", "Timothy", "William", "Charlie", "James"]

    #Different enemy types
    if enemy == "bandit":
        bandit_health = randint(50, 100)
        bandit = combatant(f"Bandit {sample(names, 1)[0]}", bandit_health, bandit_health, randint(5, 50), randint(10, 25), sample(["Dagger", "Rock", "Stick"], 1)[0], "Bandit Garbs")
        return bandit
    
    elif enemy == "mountain ranger":
        ranger_health = randint(30, 50)
        ranger = combatant(f"Mountain Ranger {sample(names, 1)[0]}", ranger_health, ranger_health, randint(20, 50), randint(20, 50), sample(["Bow", "Crossbow"], 1)[0], "Ranger Camo")
        return ranger
    
    elif enemy == "tree man":
        tree_health = randint(100, 250)
        tree_man = combatant(f"Tree Man {sample(names, 1)[0]}", tree_health, tree_health, randint(30, 40), randint(20, 30), sample(["Log", "Stick"], 1)[0], "Parmesan Protection")
        return tree_man

    elif enemy == "cheese knight":
        knight_health = randint(200, 400)
        knight = combatant(f"Cheese Knight {sample(names, 1)[0]}", knight_health, knight_health, randint(40, 60), randint(20, 50), sample(["Sword", "Greatsword"], 1)[0], "Knight Plating")
        return knight

    elif enemy == "miner":
        miner_health = randint(100, 150)
        miner = combatant(f"Miner {sample(names, 1)[0]}", miner_health, miner_health, randint(20, 50), randint(30, 40), sample(["Pickaxe", "Dynamite"], 1)[0], "Miner's Coat")
        return miner


class area:
    def __init__(self, intro_text, enemy_pool, loot_pool):
        self.intro_text = intro_text

        #Enemies and loot that are able to be selected in this area
        self.enemy_pool = enemy_pool
        self.loot_pool = loot_pool

        #Area is cleared after 3 wins
        self.battles_won = 0

        print(f"\n{intro_text}")

    def area_fight(self, player, inventory):
        enemy = generate_enemy(sample(self.enemy_pool, 1)[0])
        fight = battle_encounter(player, inventory, enemy)

        #Fight loot pool includes the areas general loot, as well as the enemy's weapon
        fight_loot_pool = list(self.loot_pool)
        fight_loot_pool.append(enemy.weapon)
        fight_loot_pool.append(enemy.armor)

        #If player wins the fight, add to the battles won counter, award points, and roll for an item
        if fight == "won":
            
            #If player won using dynamite, remove it from player's inventory
            if player.weapon == "Dynamite":
                drop_item("Dynamite", player, inventory)

            self.battles_won += 1
            award_points(3, player)

            #Grab an item from the fight loot pool. Odds determined by item's value in the items dictionary
            item = sample([enemy.weapon, enemy.armor], 1)[0]
            item_roll(items[item], item, player, inventory)
        
        #If player tries to fight without any health, tell them
        elif fight == "knocked":
            print("You have no health!")
        
        #If player lost the fight, drop a random item from their inventory
        elif fight == "lost":
            if len(inventory) != 0:
                drop_item(sample(list(inventory.keys()),1)[0], player, inventory)
    
    def gameplay_loop(self, player, inventory):

        #Gameplay loop runs until the player has won 3 fights
        while self.battles_won < 3:
            #Present actions to player
            action = multiple_choice(["1", "2", "3", "4", "5", "6"], "What would you like to do?\n1) Fight an Enemy\n2) Check Inventory\n3) Check Stats\n4) Scavenge\n5) Use Item\n6) Drop Item\n\n")

            #If action is fight, initiate a fight
            if action == "1":
                self.area_fight(player, inventory)
            
            #If action is check inventory, iterate through the player's inventory and print out each item if their inventory isn't empty
            elif action == "2":
                if len(inventory) > 0:
                    for item, amount in inventory.items():
                        print(f"x{amount} {item}\n")
                else:
                    print("You have no items!\n")

            #If action is check stats, call the player's inspect method
            elif action == "3":
                player.inspect()
            
            #If action is scavenge, grab a random item from the area's loot pool and roll for obtainment
            elif action == "4":
                item = sample(self.loot_pool, 1)[0]

                roll = item_roll(items[item], item, player, inventory)

                if roll == None:
                    print("You found nothing.\n")
                
                elif roll == "Dynamite":
                    print("(Single Use)")

            #If action is use item, call the use_item() function if the player's inventory isn't empty 
            elif action == "5":
                if len(inventory) > 0:
                    use_item(player, inventory)
                    print("\n")
                else:
                    print("You have no items!\n")
            
            #If action is discard item, iterate through the player's inventory and print out each item. Then have the player choose which item to discard
            elif action == "6":
                if len(inventory) > 0:
                    for item, amount in inventory.items():
                        print(f"x{amount} {item}\n")
                    item_choice = multiple_choice(inventory.keys(), "Which item would you like to discard? ").title()
                    drop_item(item_choice, player, inventory)
                else:
                    print("You have no items!\n")
