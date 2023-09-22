from unittest import TestCase

from app.api.exceptions import utils


class TestUtils(TestCase):

    def test_add_missing_punctuation__no_punctuation(self) -> None:
        actual = utils.add_missing_punctuation('An example message')
        self.assertEqual('An example message.', actual)

    def test_add_missing_punctuation__with_period(self) -> None:
        actual = utils.add_missing_punctuation('An example message.')
        self.assertEqual('An example message.', actual)

    def test_add_missing_punctuation__with_exclamation(self) -> None:
        actual = utils.add_missing_punctuation('An example message!')
        self.assertEqual('An example message!', actual)

    def test_add_missing_punctuation__with_question_mark(self) -> None:
        actual = utils.add_missing_punctuation('An example message?')
        self.assertEqual('An example message?', actual)
