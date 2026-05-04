# Blackjack Advantage AI

## Project Description
Blackjack Advantage AI is a Streamlit-based risk analysis tool for blackjack advantage play. The app uses Monte Carlo simulation to estimate bankroll outcomes, expected profit or loss, and risk of ruin.

The project also uses the OpenAI API to generate simple explanations of the simulation results and provide bankroll management advice.

## Features
- Interactive bankroll simulation
- Fluctuating true count model
- Wong-out threshold
- Bet spread from minimum bet to maximum bet
- Risk of ruin calculation
- Expected profit/loss calculation
- Bankroll distribution graph
- True count distribution graph
- AI-generated explanation of results

## Technologies Used
- Python
- Streamlit
- NumPy
- Matplotlib
- OpenAI API

## How to Run

Install the required libraries:

pip install -r requirements.txt

Run the app:

streamlit run app.py

## Example Inputs
- Starting bankroll: $15,000
- Minimum bet: $15
- Maximum bet: $200
- Wong-out true count: -1
- Hands per hour seen: 100
- Hours simulated: 500
- Number of simulations: 100

## Author
Jake Hernandez
