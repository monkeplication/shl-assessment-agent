from app.schemas import ExtractionResult


def should_recommend(
    extraction: ExtractionResult,
) -> tuple[bool, str]:
    """
    Decide whether enough information has been collected
    to recommend assessments.
    """

    # -------------------------
    # Safety
    # -------------------------

    if extraction.prompt_injection:
        return (
            False,
            "I can't assist with requests that attempt to manipulate my instructions.",
        )

    if extraction.off_topic:
        return (
            False,
            "I'm here to help with SHL assessment recommendations.",
        )

    if extraction.legal_question:
        return (
            False,
            "I can't provide legal advice.",
        )

    # -------------------------
    # Compare
    # -------------------------

    if extraction.intent == "compare":

        if len(extraction.compare_items) < 2:
            return (
                False,
                "Which assessments would you like me to compare?",
            )

        return True, ""

    # -------------------------
    # Need role
    # -------------------------

    if not extraction.role:

        return (
            False,
            "Who is this assessment meant for?",
        )

    # -------------------------
    # Leadership?
    # -------------------------

    leadership_words = (
        "leader",
        "leadership",
        "director",
        "executive",
        "cxo",
        "vp",
        "head",
        "manager",
    )

    role_text = extraction.role.lower()

    leadership = any(
        word in role_text
        for word in leadership_words
    )

    # -------------------------
    # Need purpose?
    # -------------------------

    if leadership:

        if extraction.refinement is None:

            return (
                False,
                "Is this for hiring (selection) or employee development?",
            )

        # Leadership assessments do NOT require skills
        return True, ""

    # -------------------------
    # Technical roles
    # -------------------------

    if (
        not extraction.skills
        and not extraction.wants_personality
        and not extraction.wants_cognitive
        and not extraction.wants_simulation
        and not extraction.wants_knowledge
    ):

        return (
            False,
            "Which skills or competencies would you like to assess?",
        )

    return True, ""