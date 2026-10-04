from evaluation.run_grader_rubric_regression import main

def test_grader_rubric_regression():
    try:
        main()
    except SystemExit as e:
        assert e.code == 0
