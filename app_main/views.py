
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import random

secret_number = None
attempts = 0
results = []

def generate_secret_number():
    return ''.join(random.sample('0123456789', 4))
  
    


def get_bulls_cows(secret, guess):
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum(g in secret for g in guess) - bulls
    return bulls, cows

MAX_ATTEMPTS = 16  # Maximum number of attempts allowed

@csrf_exempt
def home(request):
    global secret_number
    global attempts
    global results

   

    if request.method == 'GET':
        secret_number = generate_secret_number()
        print("Generated Secret Number:", secret_number)
        attempts = 0
        results = []  # Initialize results as an empty list
        return render(request, 'home.html', {'message': 'Guess a 4-digit number.'})

    elif request.method == 'POST':
        attempts += 1
        guess = request.POST.get('guess', '')

        if not guess.isdigit() or len(guess) != 4:
            return render(request, 'home.html', {'message': 'Invalid input. Please enter a 4-digit number.', 'results': results})

        bulls, cows = get_bulls_cows(secret_number, guess)
        result = {'guess': guess, 'bulls': bulls, 'cows': cows}
        results.append(result)

        if attempts >= MAX_ATTEMPTS:
            # Display a message if the maximum attempts are reached
            return render(request, 'home.html', {'message': f'Game over! You reached the maximum number of attempts. The correct number was {secret_number}.', 'success': False, 'results': results, 'success_message': ''})
        elif bulls == 4:
            # Display a congratulations message if the correct number is guessed
            return render(request, 'home.html', {'message': f'Congratulations! You guessed the number {secret_number} in {attempts} attempts.', 'success': True, 'results': results, 'success_message': 'You won!'})
        else:
            return render(request, 'home.html', {'message': f'Guess: {guess}, Bulls: {bulls}, Cows: {cows}', 'success': False, 'attempts': attempts, 'previous_guess': guess, 'results': results, 'success_message': ''})

    else:
        return HttpResponse(status=405)