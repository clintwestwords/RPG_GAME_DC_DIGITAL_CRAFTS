import random
import math

class Character:
    
    
    chance_success = False
    
    dam_ref = 0
    
    bank = 900
    
    item_list = []
    
    #? The variables below this line are for holding the values of an npc so that 
    #? When they run out of HP their character object can be used again at full health
    #? (The other values are also being reset just in case anything funny happens with
    #? item usage, abilites etc that may change the value if they die while being buffed
    #? or debuffed)
    
    HP = 0
    ST = 0
    AP = 0
    EV = 0
    
    
    
    def __init__(self, name, health, power, armor_rating, evade):
        self.name = name
        self.health = health
        self.power = power
        self.armor_rating = armor_rating
        self.evade = evade
        

        
    
    #! Checks to see if the character is still alive
    def alive(self):
        if self.health > 0:
            return True
        else:
            return False
        
        
    #! Prints health and power of the character
    def print_status(self):

        print(f"Health:  {self.health}\nDamage:  {self.power}\nArmor:  {self.armor_rating}\nEvasion: {self.evade} \n")

    
    ##################################################################################################################
    ##################################################################################################################
    #! Takes in 2 characters and performs multiple calculations and prints accordingly 
    #? Character based calculations are performed and checked within this method
    def attack(self, defense):
        
        giant_calc = False
        
        
        you_missed_text = {
            1: f"{defense.name} slipped your attack!",
            2: f"You failed to notice {defense.name}'s maneuver!", 
            3: f"{defense.name} parries adroitly!" }
        
        attacker_missed_text = {
            1:f"You evaded {self.name}'s attack!",
            2:f"You duck your head in the nick of time!",
            3:f"{self.name} fumbles his strike, and misses fantastically!"}
        
        orig_power = self.power #holds original value for power for player and npc's
        
        
        self.rng(20)#calls for a 20% chance of success for hero's (the player's) critical hit
        if self.chance_success == True and isinstance(self, Hero): #Will currently only work on Hero character
            print("Heroic Swing!")
            self.critical() #Temporarily double's hero's damage if successful
        self.rng(25)
        if self.chance_success == True and isinstance (self, Assassian):
            print("Devilish Plunge!")
            self.critical()
            
        
        if isinstance(self, Cave_Dweller):
            self.rng(20)
            if self.chance_success == True:
                print(f"{self.name} went berzerk!")
                self.berzerk()
                
        if isinstance(self, Temple_Gaurd):
            self.rng(50)
            if self.chance_success == True:
                print(f"Gaurdsman winds up and swings down with heavy force!")
                self.heavy()
        
        #! Health diminishment calculation! All damage mutlipliers should be done before this block!
        #!#########################################################################################
        
        if isinstance(self, Giant):
            self.rng(25)
            giant_calc = self.chance_success
        
        if isinstance(self, Wizard):
            self.rng(15)
            if self.chance_success == True:
                self.enchant()
        
        if self.evade > 4 and isinstance(self, Assassian) == False: #Ensures evasion can not exceed 20%
            self.evade == 4
            
            
        self.rng(defense.evade * 5) #Calculates defense's evasion score for a chance to miss the attack
        
        if self.chance_success == True: 
            if self.is_hero == True and defense.alive() == True:
                print(you_missed_text[random.randrange(1, 4)])
            elif self.is_hero == False and self.alive():
                print(attacker_missed_text[random.randrange(1, 4)])
            self.chance_success = False
            self.dam_ref = 0
        elif giant_calc == True:
               print("The Giant could not keep track of your speed!")
               self.dam_ref = 0
        else: # When evasion is unsuccessful, simmply calculate damage done
            damage = self.power - defense.armor_rating
            if damage < 1:
                damage = 1
            defense.health -= damage
            self.dam_ref = damage
        #!#########################################################################################
        #!#########################################################################################
        
        if self.is_hero == True: #Runs if it is the player character attacking
            print(f"You do {self.dam_ref} damage to {defense.name}.")
            self.power = orig_power #Resets multiplier if it was successful
            
            
            if isinstance(defense, Medic):                #Performs Medics special ability 
                defense.rng(20)                           #for a chance to heal after being 
                if defense.chance_success == True and defense.alive():        #attacked by the player
                    defense.heal()
                    print(f"{defense.name} healed!")
            
            if isinstance(defense, Wizard):                #Performs Wizards special ability 
                defense.rng(15)                           #for a chance to heal after being 
                if defense.chance_success == True and defense.alive():  
                    defense.heal()
                    
            
            
                    
                
        elif self.is_hero == False and self.alive(): #Runs when npc attacks player character
            print(f"{self.name} does {self.dam_ref} damage to you.")
            if isinstance(self, Cave_Dweller):
                self.power = orig_power #Resets cave dweller ability bonus.
            if isinstance(self, Temple_Gaurd):
                self.power = orig_power #resets gaurdsman ability bonus
            if defense.alive() == False:
                print("You are dead.")
                
        if self.is_hero == False and self.alive() == False: #This if block will contain if statemtns pertaining to unique drops
            print(f"{self.name} is dead.")
            print(f"You got {self.bounty(self)} gold!")
            if isinstance(self, Medic): #Checks if the enemy type was Medic, prints Medic's special drop
                print(f"The medic dropped 1 SuperTonic!") 
        
        if isinstance(self, Giant):
            print("The Giant Roars...")
            
            
    ##################################################################################################################
    ##################################################################################################################
    #! Random number generator used to determine if a probability based attack / defense will succeed
    def rng(self, chance):
        number = random.randrange(1, 101)
        if number <= chance:
            self.chance_success = True
        else: 
            self.chance_success = False
    
    #! Calculates the players reward for each kill
    def bounty(self, type):
        
        reward = 0
        
        if isinstance(type, Goblin):
            reward = 4
            self.rng(15)
            if self.chance_success == True:
                self.item_list.append('SuperTonic')
                print("\nThe goblin dropped a SuperTonic!")
        elif isinstance(type, Medic ):
            reward = 7
            self.item_list.append('SuperTonic')
        elif isinstance(type, Shadow):
            reward = 20
        elif isinstance(type, Cave_Dweller):
            reward = 10
            self.rng(15)
            if self.chance_success == True:
                self.item_list.append('SuperTonic')
                print("\n The Cave Dweller dropped a SuperTonic!")
            self.rng(15)
            if self.chance_success == True:
                self.item_list.append('Root of the Mutant Tree')
                print("\n The Cave Dweller dropped a strange root!")
        elif isinstance(type, Temple_Gaurd):
            reward = 25
        elif isinstance(type, Giant):
            reward = 100
            
        self.bank += reward
        
        return reward

    #! Returns quantity of a specific item 
    def itemQuant (self, item):
        
        quantity = 0
        
        for i in self.item_list:
            if i == item:
                quantity += 1
        return quantity
    
    def hold_values (self):
        self.HP = self.health
        self.ST = self.power
        self.AP = self.armor_rating
        self.EV = self.evade
    
    def reset (self):
        self.health = self.HP
        self.poewr = self.ST
        self.armor_rating = self.AP
        self.evade = self.EV
        

            
            
    
##################################################################################################################
##################################################################################################################
    
class Hero(Character):
    
    is_hero = False
    
    def __init__(self):
        super().__init__('Hero', 25, 4, 1, 0)

    def critical(self):
        self.power += self.power
    
class Goblin(Character):
    
    is_hero = False
    
    def __init__(self):
        super().__init__('the goblin', 6, 3, 0, 1)

class Zombie(Character):
    
    is_hero = False
    
    def __init__(self):
        super().__init__('the zombie', math.inf, 4, 0 )

class Medic(Character):
    
    is_hero = False
    
    def __init__(self):
        super().__init__('Medic', 25, 2, 0, 0)
        
    def heal(self):
        self.health += 6

class Shadow(Character):
    
    is_hero = False
    
    def __init__(self):
        super().__init__('Shadow', 1, 5, 0, 18)

class Cave_Dweller(Character):

    is_hero = False
    
    def __init__(self):
        super().__init__('the cave dweller', 14, 4, 1, 2)
    
    def berzerk(self):
        self.health += 2
        self.power += 3

class Temple_Gaurd(Character):
    
    is_hero = False
    
    def __init__(self):
        super().__init__('Royal Gaurdsman', 30, 10, 4, 3)
    
    def heavy(self):
        self.power *= 2

class Giant(Character):
    
    is_hero = False
    
    def __init__(self):
        super().__init__('Giant Mutant', 100, 15, 0, 0)

class Assassian(Character):
    
    is_hero = False
    
    def __init__(self):
        super().__init__('Assassian', 15, 4, 0, 3)
    
    def critical(self):
        self.power += (self.power * 0.5)

class Wizard(Character):
    
    is_hero = False
    
    used_enchant  = False
    
    def __init__(self):
        super().__init__('The Wizard', 30, 12, 4, 3)
    
    def heal(self):
            print("The wizard casts a restorative spell!")
            self.health += 5
        
    def enchant(self):
            print("The wizard enchants his weapon with electricity!")
            self.power += 4
            self.used_enchant = True


    
    