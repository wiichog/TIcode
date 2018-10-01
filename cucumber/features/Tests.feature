Feature: Does all tests works?
  Testing of program

  Scenario: Failure or success of unit test
    Given Unit tests
    When I execute them
    Then I should be told "Succes"

  Scenario: Failure or success of integration test
    Given Integration tests
    When I execute them
    Then I should be told "Succes"

  Scenario: Failure or success of stress test
    Given Stress tests
    When I execute them
    Then I should be told "Succes"

