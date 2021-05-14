import unittest

from challenge_sets.ChallengeSetList import ChallengeSetList
from datasets import load_dataset


class TestChallengeDatasets(unittest.TestCase):

    def test_webnlg_challenge_set(self):
        challenge_list = ChallengeSetList()
        dataset = load_dataset("gem", "web_nlg_en")
        generations = challenge_list.generate({"WebNLGChallengeSet": dataset})

        self.assertIsNotNone(generations["WebNLGChallengeSet"])
        self.assertIsNotNone(generations["WebNLGChallengeSet"]["challenge_input_size"])
        self.assertIsNotNone(generations["WebNLGChallengeSet"]["challenge_single_predicates"])
        self.assertIsNotNone(generations["WebNLGChallengeSet"]["challenge_combinations"])
        self.assertIsNotNone(generations["WebNLGChallengeSet"]["challenge_args"])

    def test_csrestaurant_challenge_set(self):
        challenge_list = ChallengeSetList()
        dataset = load_dataset("gem", "cs_restaurants")
        generations = challenge_list.generate({"CSRestaurantsChallengeSet": dataset})

        self.assertIsNotNone(generations["CSRestaurantsChallengeSet"])
        self.assertIsNotNone(generations["CSRestaurantsChallengeSet"]["challenge_acts"])
        self.assertIsNotNone(generations["CSRestaurantsChallengeSet"]["challenge_input_size"])

    def test_e2e_challenge_set(self):
        challenge_list = ChallengeSetList()
        dataset = load_dataset("gem", "e2e_nlg")
        generations = challenge_list.generate({"E2EChallengeSet": dataset})

        self.assertIsNotNone(generations["E2EChallengeSet"])
        self.assertIsNotNone(generations["E2EChallengeSet"]["challenge_input_size"])
        self.assertIsNotNone(generations["E2EChallengeSet"]["challenge_reference_size"])