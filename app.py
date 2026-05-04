import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from openai import OpenAI

st.set_page_config(page_title="Blackjack Advantage AI", page_icon="🃏", layout="centered")

st.title("Blackjack Advantage AI")
st.write("Risk of Ruin & Bankroll Optimization Tool")

st.markdown("---")
st.subheader("Enter Your Game Conditions")

bankroll = st.number_input("Starting Bankroll ($)", min_value=1.0, value=1000.0, step=100.0)

min_bet = st.number_input("Minimum Bet ($)", min_value=1.0, value=10.0, step=5.0)
max_bet = st.number_input("Maximum Bet ($)", min_value=1.0, value=100.0, step=10.0)

wong_out_count = st.number_input("Wong-Out True Count", value=-1.0, step=0.5)

hands_per_hour = st.number_input("Hands Per Hour Seen", min_value=1, value=100, step=10)
hours = st.number_input("Hours Simulated", min_value=1, value=10, step=1)
simulations = st.number_input("Number of Simulations", min_value=10, value=1000, step=100)

st.write("The app simulates true count changes each hand. If the true count is below the wong-out number, the player sits out.")

def estimate_edge(true_count):
    return -0.5 + (true_count * 0.5)

def choose_bet(true_count, min_bet, max_bet):
    if true_count < 1:
        return min_bet
    elif true_count == 1:
        return min_bet
    elif true_count == 2:
        return min_bet * 2
    elif true_count == 3:
        return min_bet * 4
    elif true_count == 4:
        return min_bet * 6
    else:
        return max_bet

def simulate_blackjack(bankroll, min_bet, max_bet, wong_out_count, hands_per_hour, hours, simulations):
    final_bankrolls = []
    ruin_count = 0
    total_hands_seen = int(hands_per_hour * hours)
    all_true_counts = []
    hands_played_list = []

    for _ in range(int(simulations)):
        current_bankroll = bankroll
        hands_played = 0

        for _ in range(total_hands_seen):
            true_count = round(np.random.normal(1, 2))
            true_count = max(-5, min(6, true_count))
            all_true_counts.append(true_count)

            if true_count < wong_out_count:
                continue

            bet = choose_bet(true_count, min_bet, max_bet)
            bet = min(bet, current_bankroll)

            edge = estimate_edge(true_count)

            outcome = np.random.normal(edge / 100, 1)
            current_bankroll += bet * outcome
            hands_played += 1

            if current_bankroll <= 0:
                current_bankroll = 0
                ruin_count += 1
                break

        final_bankrolls.append(current_bankroll)
        hands_played_list.append(hands_played)

    return np.array(final_bankrolls), np.array(all_true_counts), np.array(hands_played_list)

st.markdown("---")

if st.button("Run Simulation"):
    results, true_counts, hands_played = simulate_blackjack(
        bankroll, min_bet, max_bet, wong_out_count, hands_per_hour, hours, simulations
    )

    average_ending_bankroll = np.mean(results)
    expected_profit = average_ending_bankroll - bankroll
    risk_of_ruin = np.mean(results <= 0) * 100
    average_hands_played = np.mean(hands_played)

    st.subheader("Simulation Results")
    st.write(f"Average Ending Bankroll: **${average_ending_bankroll:,.2f}**")
    st.write(f"Expected Profit/Loss: **${expected_profit:,.2f}**")
    st.write(f"Risk of Ruin: **{risk_of_ruin:.2f}%**")
    st.write(f"Average Hands Actually Played: **{average_hands_played:.0f}**")

    fig, ax = plt.subplots()
    ax.hist(results, bins=30)
    ax.set_title("Final Bankroll Distribution")
    ax.set_xlabel("Ending Bankroll ($)")
    ax.set_ylabel("Number of Simulations")
    st.pyplot(fig)

    fig2, ax2 = plt.subplots()
    ax2.hist(true_counts, bins=12)
    ax2.set_title("Simulated True Count Distribution")
    ax2.set_xlabel("True Count")
    ax2.set_ylabel("Frequency")
    st.pyplot(fig2)

    st.markdown("---")
    st.subheader("AI Analysis")

    try:
        client = OpenAI(api_key="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")

        prompt = f"""
        Explain these blackjack bankroll simulation results in simple college-student language.

        This simulation does not use a fixed true count. It simulates changing true counts each hand.
        The player sits out when the true count is below the wong-out threshold.

        Inputs:
        - Starting bankroll: ${bankroll}
        - Minimum bet: ${min_bet}
        - Maximum bet: ${max_bet}
        - Wong-out true count: {wong_out_count}
        - Hands per hour seen: {hands_per_hour}
        - Hours simulated: {hours}
        - Number of simulations: {simulations}

        Results:
        - Average ending bankroll: ${average_ending_bankroll}
        - Expected profit or loss: ${expected_profit}
        - Risk of ruin: {risk_of_ruin}%
        - Average hands actually played: {average_hands_played}

        Explain what the results mean, how wonging out changes risk,
        how bet spread affects variance, and whether the bankroll looks safe.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        st.write(response.choices[0].message.content)

    except Exception:
        st.warning("Add your OpenAI API key to enable AI explanations.")