from app.agent.planner import Planner

def test_planner_returns_expected_steps():
    planner = Planner()

    steps = planner.plan()

    assert steps == ["summary", "questions", "answers"]