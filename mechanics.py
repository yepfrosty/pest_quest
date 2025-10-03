from item_data import *
from random import *


def multiple_choice(choices, prompt):
  user_choice = input(prompt).title()

  while user_choice not in choices:
    print("Invalid choice")
    user_choice = input(prompt).title()
  
  return user_choice

class combatant:
  def __init__(self, name, health, max_health, strength, speed, weapon, armor):
    self.name = name
    self.health = health + armors[armor]
    self.max_health = max_health + armors[armor]

    #Strength is added to damage calculation
    self.strength = strength
    #Speed determines who goes first in a fight
    self.speed = speed
    #Weapon is added to damage calculation, as well as critical calculation
    self.weapon = weapon
    #Armor increases max health
    self.armor = armor

  def heal(self, amount):
    new_health = self.health + amount
    print(f"{self.name} healed {amount} health!")

    #Making sure health doesnt exceed max
    if new_health > self.max_health:
      self.health = self.max_health

    #If health doesnt exceed max, set health
    else:
      self.health = new_health

  def attack(self, target, defended = 1.0):

    #Print "KABOOM" if player attacks with dynamite
    if self.weapon == "Dynamite":
      print("KABOOM!")

    #Random roll for critcal, odds depend on weapon
    critical_roll = randint(1, weapon_critical_chances[self.weapon])
    critical_multiplier = 1

    #If critical roll succeeds, double damage
    if critical_roll == 1:
      print("Critical hit!")
      critical_multiplier = 2

    #Damage calculation
    new_health = target.health-defended*(critical_multiplier*(weapon_damages[self.weapon]+self.strength))

    #If the attack was defended, include in the output
    if defended == 0.5:
      print(f"{target.name} defended! {self.name} dealt {defended*(critical_multiplier*(weapon_damages[self.weapon]+self.strength))} damage to {target.name}!")
    else:
      print(f"{self.name} dealt {defended*(critical_multiplier*(weapon_damages[self.weapon]+self.strength))} damage to {target.name}!")

    #Making sure health isnt below 0
    if new_health < 0:
      target.health = 0

    else:
      target.health = new_health
    
    
      
  def inspect(self):
    print(f"Name: {self.name}\nHealth: {self.health}/{self.max_health}\nStrength: {self.strength}\nSpeed: {self.speed}\nWeapon: {self.weapon}(Damage: {weapon_damages[self.weapon]}, Critical Chance: {100*(1/weapon_critical_chances[self.weapon])}%)\nArmor: {self.armor}(+{armors[self.armor]} Max Health)")




def drop_item(discard_item, player, inventory):
  #Subtract amount of item in inventory
  inventory[discard_item] -= 1
  print(f"{discard_item} Discarded!\n")

  #If amount of item is 0, remove item from inventory
  if inventory[discard_item] == 0:
    inventory.pop(discard_item)

  #If discarded item was held weapon, check if the player has any other weapons
  if discard_item == player.weapon and discard_item not in inventory:
    has_weapon = False
    user_weapons = []
    print("You discarded your weapon!")
    for item, amount in inventory.items():
      if item in weapon_damages:
        print(f"x{amount} {item}\n")
        has_weapon = True
        user_weapons.append(item)
        
    #If player doesnt have an extra weapon, switch their weapon to fists
    if not has_weapon:
      print("\nYou have no spare weapons, you must use your fists!")
      player.weapon = "Fists"

    #If player does have an extra weapon, ask them which they would like to equip
    else:
      new_weapon = multiple_choice(user_weapons, "Which weapon would you like to equip? ")

      #Equiping Weapon
      player.weapon = new_weapon
      print(f"{new_weapon} equipped!")

  #If discarded item was equipped armor, check if the player has any other armor
  elif discard_item == player.armor and discard_item not in inventory:
    has_armor = False
    user_armors = []
    print("You discarded your armor!")

    #Removing health buff after discarding armor and making sure health doesn't exceed max
    player.max_health -= armors[discard_item]
    if player.health > player.max_health:
      player.health = player.max_health

    for item, amount in inventory.items():
      if item in armors:
        print(f"x{amount} {item}\n")
        has_armor = True
        user_armors.append(item)
        
    #If player doesnt have extra armor, switch their armor to nothing
    if not has_armor:
      print("\nYou have no spare armor!")
      player.armor = "Nothing"

    #If player does have extra armor, ask them which they would like to equip
    else:
      new_armor = multiple_choice(user_armors, "Which armor would you like to equip? ")

      #Equiping Armor
      player.armor = new_armor
      print(f"{new_armor} equipped!")


  

def use_item(player, inventory):
  for item, amount in inventory.items():
    print(f"x{amount} {item}\n")
  item_choice = multiple_choice(inventory.keys(), "Which item would you like to use? ").title()

  #If item is a healing item, use it for healing
  if item_choice in healing_items:
    print(f"{player.name} used {item_choice}!")
    player.heal(healing_items[item_choice])
    inventory[item_choice] = inventory[item_choice]-1
    #Removing item from inventory if amount is 0
    if inventory[item_choice] == 0:
      inventory.pop(item_choice)

  #If item is a weapon, switch out current weapon
  elif item_choice in weapon_damages:
    print(f"Switched out {player.weapon} for {item_choice}!")
    player.weapon = item_choice
  
  #If item is armor, switch out current armor
  elif item_choice in armors:
    print(f"Switched out {player.armor} for {item_choice}!")

    #Removing current armor
    player.health -= armors[player.armor]
    player.max_health -= armors[player.armor]

    #If player doesnt already have the armor equipped
    if player.armor != item_choice:
      player.armor = item_choice
      #If player is max on health and equips armor, raise their health to match their new max
      if player.health == player.max_health:
        player.health += armors[player.armor]
      player.max_health += armors[player.armor]

def item_roll(chance, loot, player, inventory):
  #Rolling for loot obtainment
  roll = randint(1, chance)

  #If roll lands, offer loot to player
  if roll == 1:
    print(f"{loot} Dropped!\n")

    #Getting total number of items
    sum = 0
    for num in inventory.values():
      sum += num

    #If player's inventory is full, have them discard an item
    if sum == 10:
      print("You're inventory is full!")
      
      while True:
        choice = multiple_choice(["Y","N"],"Would you like to discard an item? y/n: ")

        #If player chooses to discard an item
        if choice == "Y":
          #Print out items in inventory
          for item, amount in inventory.items():
            print(f"x{amount} {item}\n")

          #Ask player which item they would like to discard
          discard_item = multiple_choice(inventory.keys(), "Which item would you like to discard? ")

          drop_item(discard_item, player, inventory)
                
          #Add earned item to inventory

          #If loot isn't already in inventory, set amount to 1
          if loot not in inventory:
            inventory[loot] = 1
            print(f"{loot} Obtained!")
            return loot
          
          #If loot is already in inventory, add 1 to amount
          else:
            inventory[loot] += 1
            print(f"{loot} Obtained!")
            return loot
        #If player chooses "no" to discardment, end function
        elif choice == "N":
          return "No"

    #If inventory size isn't 4, add loot to inventory
    else:
      #If loot isn't already in inventory, set amount to 1
      if loot not in inventory:
        inventory[loot] = 1
        print(f"{loot} Obtained!")
        return loot

      #If loot is already in inventory, add 1 to amount
      else:
        inventory[loot] += 1
        print(f"{loot} Obtained!")
        return loot





def award_points(amount, player):
  print(f"You earned {amount} investment points (5 stats per point)!")
  while amount > 0:
    print(f"\nMax Health: {player.max_health}\nSpeed: {player.speed}\nStrength: {player.strength}\n")
    print(f"You have {amount} investment points left.")
    
    choice = multiple_choice(["Max Health", "Strength", "Speed"], "Where would you like to invest? ")

    #Adding choice to stat
    if choice == "Max Health":
      player.max_health += 5
      amount -= 1

    elif choice == "Speed":
      player.speed += 5
      amount -= 1

    elif choice == "Strength":
      player.strength += 5
      amount -= 1
  print(f"\nMax Health: {player.max_health}\nSpeed: {player.speed}\nStrength: {player.strength}")


def battle_encounter(player, inventory, enemy):
  #Prevent player from fighting if they don't have any health
  if player.health == 0:
    return "knocked"

  print("Battle intiated!\n")

  #Showing enemy stats
  enemy.inspect()

  #Determining who goes first based on speed
  action_priority = "enemy" if enemy.speed > player.speed else "player"

  #While both combatants are alive
  while enemy.health > 0 and player.health > 0:
    #Defense variables used in attack damage calculations
    player_defense = 1
    enemy_defense = 1

    player_choice = multiple_choice(["1", "2", "3"], "\n1) Attack\n2) Item\n3) Defend \n")
  
    #If item is chosen, make sure that the player has items
    while player_choice == "2" and len(inventory.items()) == 0:
      player_choice = input("You have no items!\n1) Attack\n2) Item\n3) Defend \n\n")

    #Enemy choice is either attack or defend, as they dont have items to use
    enemy_choice = randint(1,2)

    #Checking actions when the enemy has priority
    if action_priority == "enemy":
      #If enemy attacked, process attack
      if enemy_choice == 1:
        enemy.attack(player, player_defense)
        #Checking if the enemy won after attacking
        if player.health == 0:
          print(f"Loss! {enemy.name} won!\n")
          return "lost"
        
      #If enemy defended, halve incoming damage
      elif enemy_choice == 2:
        enemy_defense = 0.5

      #If player attacked, process attack
      if player_choice == "1":
        player.attack(enemy, enemy_defense)
        #Checking if the player won after attacking
        if enemy.health == 0:
          print(f"Victory! {player.name} won!\n")
          return "won"

      #If player chooses item, show items and request choice
      elif player_choice == "2":
        use_item(player, inventory)
          
      
      #If player defended, halve incoming damage
      elif player_choice == "3":
        player_defense = 0.5


    #Checking actions when the player has priority
    elif action_priority == "player":
      #If player attacked, process attack
      if player_choice == "1":
        player.attack(enemy, enemy_defense)
        #Checking if the player won after attacking
        if enemy.health == 0:
          print(f"Victory! {player.name} won!\n")
          return "won"

      #If player chooses item, show items and request choice
      elif player_choice == "2":
        use_item(player, inventory)
            
      #If player defended, halve incoming damage    
      elif player_choice == "3":
        player_defense = 0.5


      #If enemy attacked, process attack
      if enemy_choice == 1:
        enemy.attack(player, player_defense)
        #Checking if enemy won after attacking
        if player.health == 0:
          print(f"Loss! {enemy.name} won!\n")
          return "lost"

      #If enemy defended, halve incoming damage
      elif enemy_choice == 2:
        enemy_defense = 0.5

    #Telling player if both combatants chose defend
    if enemy_defense == 0.5 and player_defense == 0.5:
      print("Both combatants defend!")

    #Showing healths after both combatants acted
    print(f"\nYour Health: {player.health}/{player.max_health}")
    print(f"{enemy.name} Health: {enemy.health}/{enemy.max_health}")


