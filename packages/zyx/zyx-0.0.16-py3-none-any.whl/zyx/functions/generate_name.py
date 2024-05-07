import random

def generate_random_name() -> str:
    """
    A fun function to generate a random name using adjectives and nouns.

    Example:
        ```python
        import zyx

        name = zyx.generate_random_name()
        print(f"Random name: {name}")
        ```
    """
    adjectives = ["Fried", "Broken", "Crazy", "Speedy", "Awesome", "Tiny", "Mighty",
                    "Sneaky", "Giant", "Absurd", "Silly", "Mysterious", "Magical", "Epic",
                    "Legendary", "Invisible", "Incredible", "Fantastic", "Glowing", "Golden",]
    nouns = ["Toast", "Burger", "Ninja", "Rocket", "Panda", "Dragon", "Pirate",
                "Robot", "Monster", "Unicorn", "Wizard", "Vampire", "Werewolf", "Zombie",
                "Alien", "Dinosaur", "Squirrel", "Penguin", "Kitten", "Puppy", "Octopus",
                "Sloth", "Llama", "Yeti", "Mermaid", "Fairy", "Phoenix", "Gryphon", "Griffin",]
    
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    return f"{adjective}{noun}"