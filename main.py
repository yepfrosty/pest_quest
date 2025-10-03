from mechanics import *
from item_data import *
from enemies import *


#Introduction
print("Hello traveler! Welcome to Tellus! This world is run by cheese, made for cheese, and exists for the sole purpose of producing more cheese. There exists a divine relic, capable of producing insurmountable amounts of cheese. This relic sits upon the Great Cheese Tower up north. Your mission is to obtain this divine relic. A grand adventure awaits you, but first...\n")
name = input("What is your name? ")

#Making Character
inventory = {"Knight Plating" : 1}
player = combatant(name, 100, 100, 20, 20, "Fists", "Nothing")

print(f"Ah! {name}! What a splendid name!\n")
print("On your mission, you will face many adversaries. Upon defeating them, you will get stronger, as well as get some loot off of them. By the time you make it to the Great Cheese Tower, you should have enough loot to fight your way through.")


#First Area
area_choice_1 = multiple_choice(["Moldy Mountains", "Parmesan Pines"],"Would you like to disembark to the Moldy Mountains, or the Parmesan Pines? ")

#Moldy Mountains
if area_choice_1 == "Moldy Mountains":
  moldy_mountains = area("Welcome to Moldy Mountains! You are surrounded by rough, mountainous terrain... and a terrible odor?", ["bandit", "mountain ranger"], ["Lesser Healing Potion", "Greater Healing Potion", "Rock", "Boulder"])
  moldy_mountains.gameplay_loop(player, inventory)

#Parmesan Pines
elif area_choice_1 == "Parmesan Pines":
  parmesan_pines = area("Welcome to Parmesan Pines! Tall, yellow trees tower over you.", ["bandit", "tree man"], ["Lesser Healing Potion", "Greater Healing Potion", "Stick", "Log"])
  parmesan_pines.gameplay_loop(player, inventory)




print("\nArea Cleared!\n")

area_choice_2 = multiple_choice(["1", "2"],"Would you like to continue moving north towards the 1) Cottage Cavern, or head back to battle through the 2) remaing area?  ")


#Cottage Cave
if area_choice_2 == "1":
  cottage_cave = area("Welcome to Cottage Cavern! You see crystalline cheese pertruding out of the cavern walls, and white whiskered mice mining away at them.", ["miner"], ["Lesser Healing Potion", "Greater Healing Potion", "Rock", "Boulder", "Pickaxe", "Dynamite"])
  cottage_cave.gameplay_loop(player, inventory)

#Remaining Area
elif area_choice_2 == "2" and area_choice_1 == "Moldy Mountains":
  parmesan_pines = area("Welcome to Parmesan Pines! Tall, yellow trees tower over you.", ["bandit", "tree man"], ["Lesser Healing Potion", "Greater Healing Potion", "Stick", "Log"])
  parmesan_pines.gameplay_loop(player, inventory)


  cottage_cavern = area("Welcome to Cottage Cavern! You see crystalline cheese pertruding out of the cavern walls, and white whiskered mice mining away at them.", ["miner"], ["Lesser Healing Potion", "Greater Healing Potion", "Rock", "Boulder", "Pickaxe", "Dynamite"])
  cottage_cavern.gameplay_loop(player, inventory)

elif area_choice_2 == "2" and area_choice_1 == "Parmesan Pines":
  moldy_mountains = area("Welcome to Moldy Mountains! You are surrounded by rough, mountainous terrain... and a terrible odor?", ["bandit", "mountain ranger"], ["Lesser Healing Potion", "Greater Healing Potion", "Rock", "Boulder"])
  moldy_mountains.gameplay_loop(player, inventory)


  cottage_cavern = area("Welcome to Cottage Cavern! You see crystalline cheese pertruding out of the cavern walls, and white whiskered mice mining away at them.", ["miner"], ["Lesser Healing Potion", "Greater Healing Potion", "Rock", "Boulder", "Pickaxe", "Dynamite"])
  cottage_cavern.gameplay_loop(player, inventory)


#Cheese Tower
print("You venture northwards to the Great Cheese Tower. The divine cheddar is glowing bright as day, the tower almost seems like a lighthouse.")

cheese_tower = area("Welcome to Cheese Tower! The tower is constructed out of hardened cheese bricks, and ascending so high that it pierces the clouds above.", ["cheese knight"], ["Stick", "Rock", "Brick", "Lesser Healing Potion", "Greater Healing Potion"])
cheese_tower.gameplay_loop(player, inventory)


print("\nAfter clearing out the cheese knights, you ascend the Great Cheese Tower and obtain the divine cheddar. Congratulations!")
