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
    Identify recurring chess mistake patterns using
    machine-readable reason_type values.
    """

    pattern_counts = {}

    for move in moves:

        if move.get("category") == "GOOD":
            continue

        reason_type = move.get("reason_type")

        if not reason_type:

            reason = move.get(
                "reason",
                "Unknown"
            )

            pattern_counts[reason] = (
                pattern_counts.get(reason, 0) + 1
            )

            continue

        if reason_type == "INACCURACY":
            continue

        pattern_counts[reason_type] = (
            pattern_counts.get(reason_type, 0) + 1
        )

    descriptions = {

        "MISSED_CAPTURE":
            "You missed opportunities to capture valuable pieces.",

        "MISSED_CHECK":
            "You missed stronger checking opportunities.",

        "MISSED_PROMOTION":
            "You missed opportunities to promote a pawn.",

        "TACTICAL_OPPORTUNITY":
            "You missed important tactical opportunities.",

        "HANGING_PIECE":
            "You allowed your pieces to become immediately vulnerable.",

        "FORK":
            "Forks and double attacks played a role in your mistakes.",

        "MATERIAL_LOSS":
            "You lost noticeable material during this phase.",

        "SIGNIFICANT_MATERIAL_LOSS":
            "You suffered significant material losses during this phase.",

        "MAJOR_EVALUATION_LOSS":
            "You had moves that caused major deterioration in the position.",

        "SIGNIFICANT_EVALUATION_LOSS":
            "Several moves significantly worsened your position.",

        "MISSED_OPPORTUNITY":
            "You missed stronger opportunities in the position."
    }

    patterns = []

    for reason_type, count in pattern_counts.items():

        if reason_type not in descriptions:

            patterns.append({
                "reason": reason_type,
                "count": count
            })

        else:

            patterns.append({
                "type": reason_type,
                "count": count,
                "description": descriptions[reason_type]
            })

    patterns.sort(
        key=lambda pattern: pattern["count"],
        reverse=True
    )

    return patterns


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

    player_color = player_color.upper()

    if player_color == "WHITE":
        opponent_color = "BLACK"
    else:
        opponent_color = "WHITE"

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


def identify_overall_weakness(report):
    """
    Identify the player's most significant recurring weakness
    across all phases of the game.
    """

    pattern_counts = {}

    for phase, data in report.items():

        for pattern in data["you"].get("patterns", []):

            pattern_type = pattern.get("type")

            if not pattern_type:
                continue

            pattern_counts[pattern_type] = (
                pattern_counts.get(pattern_type, 0)
                + pattern.get("count", 0)
            )

    if not pattern_counts:
        return {
            "type": None,
            "count": 0,
            "description": None,
            "focus": None
        }

    skill_groups = {

        "TACTICAL_AWARENESS": {

            "types": [
                "HANGING_PIECE",
                "FORK",
                "MISSED_CAPTURE",
                "MISSED_CHECK",
                "MISSED_PROMOTION",
                "TACTICAL_OPPORTUNITY"
            ],

            "description": (
                "You showed recurring tactical weaknesses, "
                "particularly in recognizing forcing moves "
                "and tactical threats."
            ),

            "focus": (
                "Focus on tactical awareness. Before every move, "
                "look for checks, captures, and threats for both "
                "you and your opponent."
            )
        },

        "MATERIAL_MANAGEMENT": {

            "types": [
                "MATERIAL_LOSS",
                "SIGNIFICANT_MATERIAL_LOSS"
            ],

            "description": (
                "You showed recurring problems with material "
                "management and protecting your pieces."
            ),

            "focus": (
                "Focus on protecting your pieces and checking "
                "whether your opponent has tactical ways to win "
                "material before committing to a move."
            )
        },

        "CALCULATION": {

            "types": [
                "MISSED_OPPORTUNITY",
                "SIGNIFICANT_EVALUATION_LOSS",
                "MAJOR_EVALUATION_LOSS"
            ],

            "description": (
                "You had recurring difficulty finding stronger "
                "continuations and accurately comparing candidate "
                "moves."
            ),

            "focus": (
                "Focus on calculating candidate moves more deeply. "
                "After choosing a move, examine your opponent's "
                "strongest response before playing it."
            )
        }
    }

    skill_scores = {}

    for skill, data in skill_groups.items():

        score = 0

        for pattern_type in data["types"]:

            score += pattern_counts.get(
                pattern_type,
                0
            )

        skill_scores[skill] = score

    weakest_skill = max(
        skill_scores,
        key=skill_scores.get
    )

    weakest_score = skill_scores[weakest_skill]

    if weakest_score == 0:
        return {
            "type": None,
            "count": 0,
            "description": None,
            "focus": None
        }

    weakness_data = skill_groups[
        weakest_skill
    ]

    return {
        "type": weakest_skill,
        "count": weakest_score,
        "description": weakness_data["description"],
        "focus": weakness_data["focus"]
    }


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

    overall_weakness = identify_overall_weakness(
        report
    )

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

    if overall_weakness["type"]:

        weakness = (
            f"{overall_weakness['description']} "
            f"This occurred {overall_weakness['count']} "
            f"time"
            f"{'s' if overall_weakness['count'] != 1 else ''} "
            f"across the game."
        )

    elif worst_stats["blunders"] > 0:

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
            f"{'s' if worst_stats['mistakes'] != 1 else ''}."
        )

    else:

        weakness = (
            f"Your {worst_phase.lower()} was your weakest phase, "
            f"although you avoided major mistakes."
        )

    # -----------------------------------------
    # Focus recommendation
    # -----------------------------------------

    if overall_weakness["focus"]:

        focus = overall_weakness["focus"]

    elif worst_stats["blunders"] > 0:

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

    overall = generate_overall_report(
        report
    )

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