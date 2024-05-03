import gc
import unittest

from suskabot.services.translator import TranslatorService


class TestTranslator(unittest.TestCase):
    translation_services: str = "google,yandex,bing,argos"
    user_language: str = "ru"
    default_lang_to_translate_to: str = "en"

    service: TranslatorService

    def setUp(self):
        self.service = TranslatorService(
            comma_separated_translation_services=self.translation_services,
            user_language=self.user_language,
            default_lang_to_translate_to=self.default_lang_to_translate_to
        )

    def test_number_translation(self):
        self.assertEqual(self.service.translate("пять"), "five")

    def test_reverse_language_translation(self):
        self.assertEqual(self.service.translate("five"), "пять")

    def test_well_known_translation(self):
        self.assertEqual(self.service.translate("кошка"), "cat")

    def tearDown(self):
        del self.service
        gc.collect()


if __name__ == '__main__':
    unittest.main()
