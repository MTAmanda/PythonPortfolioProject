

class Question:
    def __init__(self, question_number, question_text, options, correct_answer):
        self.question_number = question_number
        self.question_text = question_text
        self.options = options
        self.correct_option = correct_answer

    def display_question(self):
        print(f"Question #{self.question_number}")
        print(self.question_text)
        for key, value in self.options.items():
            print(f"{key}: {value}")

    def is_correct(self, player_answer):
        return player_answer == self.correct_option

class Game:
    def __init__(self, questions):
        self.questions = questions
        self.current_question_index = 0
        self.score_index = 0
        self.lifeline = Lifeline()
        self.available_lifelines = ["50:50", "Call a Friend", "Audience Vote"]

    def ask_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            question.display_question()

            # Check if any lifelines are available and ask the player if they want to use one
            if not self.lifeline.is_used():
                use_lifeline = input("Do you want to use a lifeline? Yes(Y) / No(N): ")
                if use_lifeline.upper() == "Y":
                    self.use_lifeline(question)

            # Player answers here
            player_first_answer = input("Your answer (enter the option letter): ")
            while True:
                verification_question = input("Is this your final answer? Yes(Y) / No(N): ")

                if verification_question.upper() == "Y" :
                    player_answer = player_first_answer
                    break
                elif verification_question.upper() == "N" :
                    player_answer = input("Please provide your final answer (enter the option letter): ")
                    break
                else:
                    print("Please answer with: Y or N")

            if question.is_correct(player_answer.upper()):
                print("That's correct!")
                print(f"Your prize is {self.calculate_score(question, player_answer)} Eur. \n")
                self.score_index += 1


                if self.current_question_index < len(self.questions):
                    next_question = input(f"You can take your current prize and leave or risk it and continue. \nDo you want to go for the next question? Yes(Y) / No(N): \n")
                    if next_question.upper() == "Y":
                        self.current_question_index += 1
                        return True
                    else:
                        print(f"Congratulations! You won a {self.calculate_score(question, player_answer)} Eur prize.")

            else:
                print(f"\n ------> Wrong! The correct answer was {question.correct_option}. You're walking away with {self.calculate_score(question, player_answer)} Eur. \n")
                return False
        else:
            return False

    def calculate_score(self, question, player_answer):
        is_correct = question.is_correct(player_answer.upper())
        score_table = [100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]
        score_milestones = [0] * 4 + [score_table[4]] * 5 + [score_table[9]] * 5 + [score_table[14]]
        if is_correct:
            return score_table[self.score_index]
        else:
            return score_milestones[self.score_index]


    def use_lifeline(self, question):
        print("Choose a lifeline:")

        for i, lifeline_option in enumerate(self.available_lifelines, start=1):
            print(f"{lifeline_option} ({i})")

        # Get user input for lifeline type
        lifeline_type = input("Enter the option number of your chosen lifeline: ")

        if lifeline_type.isdigit():
            lifeline_index = int(lifeline_type) - 1
            if 0 <= lifeline_index < len(self.available_lifelines):
                selected_lifeline = self.available_lifelines[lifeline_index]

                if selected_lifeline == "50:50" and not self.lifeline.used_fifty_fifty:
                    self.lifeline.use_fifty_fifty(question)
                    question.display_question()
                elif selected_lifeline == "Call a Friend" and not self.lifeline.friend_called:
                    self.lifeline.call_a_friend(question)
                elif selected_lifeline == "Audience Vote" and not self.lifeline.audience_voted:
                    self.lifeline.audience_vote(question)
                else:
                    print("Invalid lifeline choice. No lifeline will be used.")

                # Remove the used lifeline from the available options
                self.available_lifelines.pop(lifeline_index)
            else:
                print("Invalid lifeline choice. No lifeline will be used.")
        else:
            print("Invalid input. No lifeline will be used.")


import random
class Lifeline:
    def __init__(self):
        # Flag to check if the lifeline options have been used
        self.used_fifty_fifty = False
        self.friend_called = False
        self.audience_voted = False

    def is_used(self):
        return self.used_fifty_fifty and self.friend_called and self.audience_voted


    #50:50 option
    def use_fifty_fifty(self, question):
        if not self.used_fifty_fifty:
            # Get the correct answer
            correct_answer = question.correct_option
            # Get a list of incorrect options
            incorrect_options = [key for key in question.options.keys() if key != correct_answer]
            # Randomly choose two incorrect options to remove
            options_to_remove = random.sample(incorrect_options,2)
            # Remove the chosen incorrect options
            for option in options_to_remove:
                del question.options[option]
            # Mark the 50:50 lifeline as used
            self.used_fifty_fifty = True
            print("50:50 lifeline used. Two incorrect options removed.")
        else:
            print("Sorry, you have already used the 50:50 lifeline in this game.")
    #Call a friend option
    def call_a_friend(self, question):
        if not self.friend_called:
            print("Calling a friend for help...")
            # Simulate a friend's response (replace this with actual logic)
            friend_response = random.choice(list(question.options.values()))
            print(f"Your friend suggests choosing option: {friend_response}")
            self.friend_called = True
        else:
            print("Sorry, you have already called a friend in this game.")
    # Audience vote option:
    def audience_vote(self, question):
        if not self.audience_voted:
            print("Audience voting...")
            # Simulate audience voting (replace this with actual logic)
            audience_votes = {key: random.randint(0, 100) for key in question.options}
            print("Audience votes:")
            for key, votes in audience_votes.items():
                print(f"{key}: {votes}%")
            self.audience_voted = True
        else:
            print("Sorry, the audience has already helped you once in this game.")

    # ______________________ Definitions ______________________

question1 = Question(1,"What is the traditional color of the jersey worn by the leader of the Tour de France?", {"A":"Yellow", "B": "Green", "C":"Red", "D":"Blue"}, "A")
question2 = Question(2,"In which sport would you perform a \"double axel\"?", {"A": "Figure skating","B": "Gymnastics", "C": "Ski jumping", "D": "Fencing"}, "A")
question3 = Question(3,"What is the highest point on Earth's surface above sea level?", {"A": "Mount Kilimanjaro" ,"B": "Mount Everest", "C": "Denali (Mount McKinley)", "D":"Mount Fuji"}, "B")
question4 = Question(4,"Which of the following is a feature of a standard golf ball?" ,{"A": "Dimples","B": "Spikes", "C":"Stripes", "D": "Scales"}, "A")
question5 = Question(5,"In archery, what is the term for the central part of the bow that the arrow is shot from?",{"A": "Shaft", "B": "Fletching", "C": "Riser","D": "Nock"},"C")
question6 = Question(6,"What is the primary objective in the sport of curling?" ,{"A": "Score goals", "B": "Sink putts", "C": "Knock down pins","D": "Slide stones to a target"},"D")
question7 = Question(7,"Which of the following is a term used in fencing to describe a successful attack that lands without being parried?",{"A": "Riposte", "B": "Lunge", "C": "Feint","D": "Touche"},"B")
question8 = Question(8,"What is the standard number of players on a soccer team?" ,{"A": "9", "B": "11", "C": "7","D": "15"},"B")
question9 = Question(9,"In equestrian events, what is the term for the course of jumps that a horse and rider must navigate?" ,{"A": "Circuit", "B": "Course", "C": "Track","D": "Ring"},"B")
question10 = Question(10,"Which of the following is a style of martial arts that originated in Korea?" ,{"A": "Judo", "B": "Kung Fu", "C": "Taekwondo","D": "Muay Thai"},"C")
question11 = Question(11,"In which Olympic event do athletes compete in a combination of cross-country skiing and rifle shooting?" ,{"A": "Biathlon", "B": "Decathlon", "C": "Pentathlon","D": "Heptathlon"},"A")
question12 = Question(12,"What is the traditional Japanese martial art of drawing and quickly striking with a sword?",{"A": "Jiu-Jitsu", "B": "Aikido", "C": "Kendo","D": "Karate"},"C")
question13 = Question(13,"Which country is known for inventing the sport of parkour?" ,{"A": "France", "B": "United States", "C": "Brazil","D": "Russia"},"A")
question14 = Question(14,"What is the term for the technique of descending a slope on skis with a series of quick, short turns?" ,{"A": "Slalom", "B": "Moguls", "C": "Downhill","D": "Cross-country"},"A")
question15 = Question(15,"In orienteering, participants use a map and compass to navigate through unfamiliar terrain and locate checkpoints. What is the term for these checkpoints?" ,{"A": "Waypoints", "B": "Coordinates", "C": "Control points","D": "Check markers"},"C")


questions_list = [question1, question2, question3, question4, question5, question6, question7, question8, question9, question10, question11, question12, question13, question14, question15]

game = Game(questions_list)

# ______________________ Gameplay ______________________

print("----------------  Welcome to the \'Who Wants to Be a Millionaire\' game!  ----------------  \n")
input("Please press Enter to start the game!")

while game.ask_question():
    pass