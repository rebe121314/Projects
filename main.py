import random
from words import words_list

#input words from word list
def get_word():
  word = random.choice(words_list)
  #word = input(" writte: ")
  #converst to upper letterst to avoid errors
  return word.upper()

#start the game
def play(word):
  word_completion = "_ " * len(word)
  guessed= False
  guessed_letters = []
  guessed_words = []
  tries = 7
  print("Let's play! :D")
  #prints the image
  print(display(tries))
  print(word_completion)
  print("\n")
  while not guessed and tries > 0:
    guess = input ("Please guess a letter or a word: ").upper()
    #input can't have numbers
    if len(guess) == 1 and guess.isalpha():
      if guess in guessed_letters:
        print("You already guess the letter", guess)
      elif guess not in word:
        print(guess, "is not in the word." )
        tries -= 1
        guessed_letters.append(guess)
      else:
        print("Yes!, " + guess+ " is in the word")
        guessed_letters.append(guess)
        word_as_list = list(word_completion)
        #locates the places were the letter appears
        indices = [i for i, letter in enumerate(word) if letter == guess]
        for index in indices:
          word_as_list[index]= guess
        word_completion = "".join(word_as_list)
        if "_"not in word_completion:
          guessed = True
    elif len(guess) == len(word).isalpha():
      if guess in guessed_words:
        print(":/ You alreadt try this, ", guess)
      elif guess != word:
        print (guess, "is not the word.")
        tries -=1
        guessed_words.append(guess)
      else:
        guessed = True
        #word_complition = word

    else:
      print("Not a valid guess.")
    print(display(tries))
    print(word_completion)
    print("\n")
  if guessed:
    print("Yeah! You won!")
  else:
    print("Sorry you ran out of tries :( The word was " + word +". Maybe next time")

#prints the images
def display(tries):
  stages = [  """
              I--------------
              I              !
              I              O
              I             \I/
              I              I
              I             / \\
              I
              I
              _
              """,
              """
              I--------------
              I              !
              I              O
              I             \I/
              I              I
              I             / 
              I
              I
              _
              """,
              """
              I--------------
              I              !
              I              O
              I             \I/
              I              I
              I              
              I
              I
              _
              """,
              """
              I--------------
              I              !
              I              O
              I             \I/
              I              
              I             
              I
              I
              _
              """,
              """
              I--------------
              I              !
              I              O
              I             \I
              I              
              I             
              I
              I
              _
              """,
              """
              I--------------
              I              !
              I              O
              I              I
              I              
              I             
              I
              I
              _
              """,
              """
              I--------------
              I              !
              I              O
              I             
              I              
              I             
              I
              I
              _
              """,
              """
              I--------------
              I              !
              I              
              I             
              I              
              I             
              I
              I
              _
              """ ]
  return stages[tries]      

#start the game when run the kernell

def main():
  word = get_word()
  play(word)
  while input("Play agian? (Y/N)").upper()== "Y":
    word = get_word()
    play(word)


if __name__ == "__main__":
  main()
