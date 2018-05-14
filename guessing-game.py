import speech_recognition as sr
import random as rand

def load_words(num_words):
    """this function reads the file in directory and loads in 5 random words """
    all_w = []
    selected_w = []
    with open('random_words.txt') as words_file:
        # cleaning file
        words = [x.strip().split() for x in words_file]
        for i in words:
            for x in i:
                all_w.append(x)
    # selecting 5 random words
    for i in range(num_words):
        selected_w.append(rand.choice(all_w))
    return selected_w

def recognizing_user_speech(recognizer, microphone):
    """this function takes the user speech from the microphone and transcribes it.
    It can return 'sucsess', 'transcription' or 'error' depending on wether or not he speech was able to be transcribed
    recognizer: recognizer used to transcribe text
    microphone: user microphone
    """
    # checking if the parameters are the appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError('recognizer must be "Recognizer" instance')
    if not isinstance(microphone, sr.Microphone):
        raise TypeError('microphone must be "Microphone" instance')

    # recording and adjusting the audio
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # response, based on if audio was transcribed,
    # (success: api avalibility, transcription: if audio was transcribed, error: error)
    response = {
    'success': True,
    'error': None,
    'Transcription': None
    }

    # try/ except block for catching errors
    try:
        # adding user audio to the transcription key
        response['Transcription'] = recognizer.recognize_google(audio)
    # if the API cant be reached
    except sr.RequestError:
        response['success'] = False
        response['error'] = 'API unavailable'
    # if audio cant be transcribed
    except sr.UnknownValueError:
        response['error'] = 'audio can not be recognized'

    # returning response
    return response


# taking user settings
num_words = int(input('How many words would you like to have? '))
num_guess = int(input('How many guesses would you like to have? '))

# initalizing the microphone and recogonizer
rec = sr.Recognizer()
mic = sr.Microphone()
# loading words
words = load_words(num_words)
# choosing one word
chosen_word = rand.choice(words)

# initial msg 
print('I am thinking of one of these words {}, which one is it? You have {} guesses'.format(words, num_guess))

for i in range(num_guess):
    # how many times the game should promt the user (10)
    for x in range(5):
        print('Guess {}, say something!'.format(i+1))
        user_guess = recognizing_user_speech(rec, mic)
        # transcription is returned
        if user_guess['Transcription']:
            break
        # api request failed
        if not user_guess['success']:
            break
        print('I could not understand what you said, please say it again.')
    # if error break out of game
    if user_guess['error']:
        print('Error: {}'.format(user_guess['error']))
        break
    # If user guesses correctly
    if (user_guess['Transcription'].lower()) == chosen_word.lower():
        print('You said "{}"'.format(user_guess['Transcription']))
        print('You got it!! the word was "{}"'.format(chosen_word))
        break
    else:
        print('Wrong! Guess again!')

# if the user has run out of guesses and has not gotten the word yet
print('sorry you are out of guesses, the word was "{}"'.format(chosen_word))
