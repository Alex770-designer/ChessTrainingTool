import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_PATH = os.path.join(BASE_DIR, "analysis.json")


def analyze_moves(moves):
    """
    Calculate statistics for a group of moves.
    """

    if not moves:
        return {
            "moves": 0,
            "blunders": 0,
            "mistakes": 0,
            "inaccuracies": 0,
            "average_loss": 0,
            "largest_loss": 0
        }

    blunders = sum(
        move["category"] == "BLUNDER"
        for move in moves
    )

    mistakes = sum(
        move["category"] == "MISTAKE"
        for move in moves
    )

    inaccuracies = sum(
        move["category"] == "INACCURACY"
        for move in moves
    )

    losses = [
        max(0, move["loss"])
        for move in moves
    ]

    average_loss = sum(losses) / len(losses)

    largest_loss = max(losses)

    return {
        "moves": len(moves),
        "blunders": blunders,
        "mistakes": mistakes,
        "inaccuracies": inaccuracies,
        "average_loss": round(average_loss, 1),
        "largest_loss": largest_loss
    }


def performance_rating(stats):

    if stats["moves"] == 0:
        return "No moves played"

    blunders = stats["blunders"]
    mistakes = stats["mistakes"]
    average_loss = stats["average_loss"]

    if blunders == 0 and mistakes == 0 and average_loss < 50:
        return "Excellent"

    if blunders == 0 and mistakes <= 1 and average_loss < 100:
        return "Good"

    if blunders <= 1 and mistakes <= 3 and average_loss < 150:
        return "Inconsistent"

    if blunders <= 2 and average_loss < 300:
        return "Needs Improvement"

    return "Poor"


def identify_patterns(moves):
    """
    Identify the most common reasons for mistakes.
    """

    patterns = {}

    for move in moves:

        if move["category"] == "GOOD":
            continue

        reason = move.get(
            "reason",
            "Unknown"
        )

        patterns[reason] = patterns.get(
            reason,
            0
        ) + 1

    sorted_patterns = sorted(
        patterns.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return [
        {
            "reason": reason,
            "count": count
        }
        for reason, count in sorted_patterns
    ]


def generate_summary(
    stats,
    opponent_stats,
    phase
):

    if stats["moves"] == 0:
        return (
            f"You did not play any moves during "
            f"the {phase.lower()}."
        )

    performance = stats["performance"]

    if performance == "Excellent":

        summary = (
            f"Your {phase.lower()} was excellent. "
            f"You avoided major mistakes and "
            f"maintained a high level of accuracy."
        )

    elif performance == "Good":

        summary = (
            f"Your {phase.lower()} was solid. "
            f"You made relatively few significant errors."
        )

    elif performance == "Inconsistent":

        summary = (
            f"Your {phase.lower()} was somewhat inconsistent. "
            f"You had several inaccuracies or mistakes "
            f"that affected the position."
        )

    elif performance == "Needs Improvement":

        summary = (
            f"Your {phase.lower()} needs improvement. "
            f"You gave up a noticeable amount of "
            f"evaluation through mistakes."
        )

    else:

        summary = (
            f"Your {phase.lower()} was your weakest phase. "
            f"Several significant errors caused "
            f"substantial deterioration in the position."
        )

    # Compare your performance with the opponent

    if stats["average_loss"] < opponent_stats["average_loss"]:

        summary += (
            " You performed better than your opponent "
            "during this phase."
        )

    elif stats["average_loss"] > opponent_stats["average_loss"]:

        summary += (
            " Your opponent performed better than you "
            "during this phase."
        )

    else:

        summary += (
            " You and your opponent performed at a "
            "similar level during this phase."
        )

    return summary


def generate_phase_report():

    with open(ANALYSIS_PATH) as file:
        analysis = json.load(file)

    if not analysis:
        return {}

    player_color = analysis[0].get(
        "player_color",
        "white"
    )

    phases = {

        "OPENING": {
            "WHITE": [],
            "BLACK": []
        },

        "MIDDLEGAME": {
            "WHITE": [],
            "BLACK": []
        },

        "ENDGAME": {
            "WHITE": [],
            "BLACK": []
        }
    }

    # -----------------------------------------
    # Group moves by phase and player
    # -----------------------------------------

    for move in analysis:

        phase = move.get("phase")

        if phase not in phases:
            continue

        turn = move["fen"].split(" ")[1]

        if turn == "w":
            color = "WHITE"
        else:
            color = "BLACK"

        phases[phase][color].append(move)

    # -----------------------------------------
    # Determine player's color
    # -----------------------------------------

    player_color = player_color.upper()

    if player_color == "WHITE":
        opponent_color = "BLACK"

    else:
        opponent_color = "WHITE"

    # -----------------------------------------
    # Generate report
    # -----------------------------------------

    report = {}

    for phase in phases:

        your_moves = phases[phase][player_color]
        opponent_moves = phases[phase][opponent_color]

        your_stats = analyze_moves(
            your_moves
        )

        opponent_stats = analyze_moves(
            opponent_moves
        )

        your_performance = performance_rating(
            your_stats
        )

        opponent_performance = performance_rating(
            opponent_stats
        )

        your_patterns = identify_patterns(
            your_moves
        )

        opponent_patterns = identify_patterns(
            opponent_moves
        )

        report[phase] = {

            "you": {
                **your_stats,
                "performance": your_performance,
                "patterns": your_patterns
            },

            "opponent": {
                **opponent_stats,
                "performance": opponent_performance,
                "patterns": opponent_patterns
            },

            "summary": generate_summary(
                {
                    **your_stats,
                    "performance": your_performance
                },

                {
                    **opponent_stats,
                    "performance": opponent_performance
                },

                phase
            )
        }

    return report

def generate_overall_report(report):
    """
    Generate an overall summary from the phase reports.
    """

    phases_with_moves = []

    for phase, data in report.items():

        if data["you"]["moves"] > 0:
            phases_with_moves.append(
                (phase, data["you"])
            )

    if not phases_with_moves:
        return {
            "best_phase": None,
            "worst_phase": None,
            "summary": "No moves were available for analysis.",
            "strength": None,
            "weakness": None,
            "focus": None
        }

    # -----------------------------------------
    # Best and worst phases
    # -----------------------------------------

    best_phase, best_stats = min(
        phases_with_moves,
        key=lambda item: item[1]["average_loss"]
    )

    worst_phase, worst_stats = max(
        phases_with_moves,
        key=lambda item: item[1]["average_loss"]
    )

    # -----------------------------------------
    # Strength
    # -----------------------------------------

    if best_stats["performance"] == "Excellent":

        strength = (
            f"Your {best_phase.lower()} was your strongest phase. "
            f"You played accurately and avoided major mistakes."
        )

    elif best_stats["performance"] == "Good":

        strength = (
            f"Your {best_phase.lower()} was your strongest phase. "
            f"You played consistently with relatively few errors."
        )

    else:

        strength = (
            f"Your {best_phase.lower()} was your strongest phase, "
            f"although there is still room for improvement."
        )

    # -----------------------------------------
    # Weakness
    # -----------------------------------------

    if worst_stats["blunders"] > 0:

        weakness = (
            f"Your {worst_phase.lower()} was your weakest phase. "
            f"You made {worst_stats['blunders']} blunder"
            f"{'s' if worst_stats['blunders'] != 1 else ''}, "
            f"which caused significant evaluation loss."
        )

    elif worst_stats["mistakes"] > 0:

        weakness = (
            f"Your {worst_phase.lower()} was your weakest phase. "
            f"You made {worst_stats['mistakes']} mistake"
            f"{'s' if worst_stats['mistakes'] != 1 else ''} "
            f"and {worst_stats['inaccuracies']} inaccuracy"
            f"{'ies' if worst_stats['inaccuracies'] != 1 else 'y'}."
        )

    else:

        weakness = (
            f"Your {worst_phase.lower()} was your weakest phase, "
            f"although you avoided major mistakes."
        )

    # -----------------------------------------
    # Focus recommendation
    # -----------------------------------------

    if worst_stats["blunders"] > 0:

        focus = (
            "Focus on tactical awareness and checking your "
            "opponent's threats before committing to a move."
        )

    elif worst_stats["mistakes"] >= 3:

        focus = (
            "Focus on calculating candidate moves more carefully "
            "and comparing your options before playing."
        )

    elif worst_stats["inaccuracies"] >= 3:

        focus = (
            "Focus on improving move accuracy and looking for "
            "stronger positional alternatives."
        )

    else:

        focus = (
            "Continue working on consistency and maintaining "
            "accurate play throughout the game."
        )

    # -----------------------------------------
    # Overall summary
    # -----------------------------------------

    if best_phase == worst_phase:

        summary = (
            f"Your overall performance was relatively consistent "
            f"throughout the game, with your {best_phase.lower()} "
            f"showing the strongest results."
        )

    else:

        summary = (
            f"Your strongest phase was the {best_phase.lower()}, "
            f"while your weakest phase was the "
            f"{worst_phase.lower()}."
        )

    return {
        "best_phase": best_phase,
        "worst_phase": worst_phase,
        "summary": summary,
        "strength": strength,
        "weakness": weakness,
        "focus": focus
    }

if __name__ == "__main__":

    report = generate_phase_report()

    overall = generate_overall_report(report)

    final_report = {
        "phases": report,
        "overall": overall
    }

    print(
        json.dumps(
            final_report,
            indent=4
        )
    )