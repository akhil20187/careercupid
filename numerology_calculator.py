class NumerologyCalculator:
    @staticmethod
    def reduce_to_single_digit(number):
        """
        Reduce a number to a single digit, with exceptions for master numbers 11 and 22
        """
        while number > 9 and number not in [11, 22]:
            number = sum(int(digit) for digit in str(number))
        return number

    @staticmethod
    def calculate_life_path_number(birth_date):
        """
        Calculate Life Path Number from date of birth 
        
        Args:
            birth_date (str): Date in DD/MM/YYYY format
        
        Returns:
            int: Life Path Number (1-9 or master number 11/22)
        """
        # Remove any non-digit characters
        digits = ''.join(filter(str.isdigit, birth_date))
        
        # Sum all digits
        total = sum(int(digit) for digit in digits)
        
        # Reduce to single digit or master number
        return NumerologyCalculator.reduce_to_single_digit(total)

    @staticmethod
    def calculate_expression_number(full_name):
        """
        Calculate Expression Number from full legal name
        
        Args:
            full_name (str): Full legal name
        
        Returns:
            int: Expression Number (1-9 or master number 11/22)
        """
        # Get letter values
        letter_values = NumerologyCalculator._get_letter_values()
        
        # Convert name to lowercase and remove non-alphabetic characters
        name = ''.join(filter(str.isalpha, full_name.lower()))
        
        # Calculate total value
        total = sum(letter_values.get(char, 0) for char in name)
        
        # Reduce to single digit or master number
        return NumerologyCalculator.reduce_to_single_digit(total)

    @staticmethod
    def _get_letter_values():
        """
        Pythagorean letter mapping with consistent values
        """
        return {
            'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 
            'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 1, 
            'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 6, 
            'p': 7, 'q': 8, 'r': 9, 's': 1, 't': 2, 
            'u': 3, 'v': 4, 'w': 5, 'x': 6, 'y': 7, 'z': 8
        }

    @staticmethod
    def calculate_soul_urge_number(full_name):
        """
        Calculate Soul Urge (Heart's Desire) Number using vowels only
        
        Args:
            full_name (str): Full name
        
        Returns:
            int: Soul Urge Number (1-9 or master number 11/22)
        """
        # Vowels
        vowels = 'aeiou'
        
        # Get letter values
        letter_values = NumerologyCalculator._get_letter_values()
        
        # Convert name to lowercase and filter vowels
        name_vowels = ''.join(
            char for char in full_name.lower() 
            if char in vowels
        )
        
        # Calculate total value
        total = sum(letter_values.get(char, 0) for char in name_vowels)
        
        # Reduce to single digit or master number
        return NumerologyCalculator.reduce_to_single_digit(total)

    @staticmethod
    def calculate_personality_number(full_name):
        """
        Calculate Personality (Outer Expression) Number using consonants only
        
        Args:
            full_name (str): Full name
        
        Returns:
            int: Personality Number (1-9 or master number 11/22)
        """
        # Consonants
        consonants = 'bcdfghjklmnpqrstvwxyz'
        
        # Get letter values
        letter_values = NumerologyCalculator._get_letter_values()
        
        # Convert name to lowercase and filter consonants
        name_consonants = ''.join(
            char for char in full_name.lower() 
            if char in consonants
        )
        
        # Calculate total value
        total = sum(letter_values.get(char, 0) for char in name_consonants)
        
        # Reduce to single digit or master number
        return NumerologyCalculator.reduce_to_single_digit(total)

    @staticmethod
    def calculate_birth_number(birth_date):
        """
        Calculate Birth Number from date of birth
        
        Args:
            birth_date (str): Date in DD/MM/YYYY format
        
        Returns:
            int: Birth Number (1-9)
        """
        # Extract the day from the birth date
        try:
            # Split the date and ensure we're using the day
            day = birth_date.split('/')[0]
            
            # Ensure we're working with the day as a number
            day = int(day)
            
            # Reduce to single digit
            return NumerologyCalculator.reduce_to_single_digit(day)
        
        except (IndexError, ValueError):
            raise ValueError("Invalid birth date format. Please use DD/MM/YYYY")

    @staticmethod
    def explain_number(number):
        """
        Provide a brief explanation of the numerological number
        """
        number_explanations = {
            1: "Leadership, independence, originality",
            2: "Cooperation, diplomacy, sensitivity",
            3: "Creativity, self-expression, joy",
            4: "Stability, hard work, practicality",
            5: "Freedom, change, adventure",
            6: "Love, harmony, responsibility",
            7: "Introspection, spirituality, wisdom",
            8: "Power, abundance, achievement",
            9: "Compassion, service, selflessness",
            11: "Spiritual insight, intuition, inspiration",
            22: "Master builder, large-scale achievements"
        }
        
        return number_explanations.get(number, "Unique spiritual significance")

    @staticmethod
    def explain_birth_number(number):
        """
        Provide a detailed explanation of the Birth Number
        """
        birth_number_meanings = {
            1: "Natural leader, independent, pioneering spirit",
            2: "Cooperative, sensitive, diplomatic",
            3: "Creative, expressive, communicative",
            4: "Practical, disciplined, hard-working",
            5: "Adventurous, freedom-loving, versatile",
            6: "Nurturing, responsible, harmonious",
            7: "Introspective, analytical, spiritual",
            8: "Ambitious, powerful, material success",
            9: "Compassionate, humanitarian, selfless"
        }
        
        return birth_number_meanings.get(number, "Unique personal energy")

# Example usage
def main():
    # Example calculations
    birth_date = "20/01/1987"
    full_name = "Akhilesh Gupta Ainapur"
    
    # Calculate all numerological numbers
    life_path = NumerologyCalculator.calculate_life_path_number(birth_date)
    expression = NumerologyCalculator.calculate_expression_number(full_name)
    soul_urge = NumerologyCalculator.calculate_soul_urge_number(full_name)
    personality = NumerologyCalculator.calculate_personality_number(full_name)
    birth_number = NumerologyCalculator.calculate_birth_number(birth_date)
    
    print(f"Life Path Number: {life_path}")
    print(f"Expression Number: {expression}")
    print(f"Soul Urge Number: {soul_urge}")
    print(f"Personality Number: {personality}")
    print(f"Birth Number: {birth_number}")

if __name__ == "__main__":
    main()

    # Optional: Demonstrate number explanations
    print("\nNumber Explanations:")
    for num in [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22]:
        print(f"Number {num}: {NumerologyCalculator.explain_number(num)}")

    # Optional: Demonstrate Birth Number explanations
    print("\nBirth Number Explanations:")
    for num in range(1, 10):
        print(f"Birth Number {num}: {NumerologyCalculator.explain_birth_number(num)}")