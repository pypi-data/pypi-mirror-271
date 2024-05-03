import logging
from typing import List, Dict

import translators

from lingua import Language, LanguageDetector, LanguageDetectorBuilder
from translators.server import TranslatorError

logger = logging.getLogger(__name__)


class TranslatorService:
    _translation_services: List[str]
    _user_language: str
    _default_language_to_translate_to: str

    def __init__(
            self,
            comma_separated_translation_services: str,
            user_language: str,
            default_lang_to_translate_to: str
    ) -> None:
        translation_services: List[str] = comma_separated_translation_services.strip().split(',')
        self._translation_services = translation_services

        self._user_language = user_language
        self._default_language_to_translate_to = default_lang_to_translate_to

    def __get_language_to_translate_to(self, language_code: str) -> str:
        # detected language: language to translate to
        translation_rules: Dict[str, str] = {
            self._default_language_to_translate_to: self._user_language,
        }
        default_language_to_translate_to: str = self._default_language_to_translate_to

        language_to_translate_to: str = translation_rules.get(language_code, default_language_to_translate_to)

        logger.debug(f"Will translate from {language_code} to {language_to_translate_to}")
        return language_to_translate_to

    def translate(self, text_to_translate: str) -> str:
        supported_languages: List[Language] = [Language.ENGLISH, Language.RUSSIAN, Language.UKRAINIAN]

        language_detector: LanguageDetector = LanguageDetectorBuilder.from_languages(*supported_languages).build()
        language_to_translate_from: str = language_detector.detect_language_of(text_to_translate).name.lower()[0:2]
        logger.debug(f"Detected {language_to_translate_from} language from \"{text_to_translate}\"")

        translation_services: List[str] = self._translation_services

        language_to_translate_to: str = self.__get_language_to_translate_to(language_to_translate_from)

        logger.debug(f"Will use this list of translation services: {translation_services}")
        for translation_service in translation_services:
            logger.debug(f"Trying to translate using {translation_service}..")
            try:
                translation: str = translators.translate_text(
                    query_text=text_to_translate,
                    translator=translation_service,
                    from_language=language_to_translate_from,
                    to_language=language_to_translate_to,
                    if_use_preacceleration=False
                )
            except TranslatorError as e:
                logger.warning(f"{e} occurred when trying to translate \"{text_to_translate}\" "
                               f"from \"{language_to_translate_from}\" "
                               f"to \"{language_to_translate_to}\" "
                               f"using {translation_service} service")
                continue
            except Exception as e:
                logger.warning(f"An unexpected error {e} occurred when trying to translate \"{text_to_translate}\" "
                               f"from \"{language_to_translate_from}\" "
                               f"to \"{language_to_translate_to}\" "
                               f"using {translation_service} service")
                continue

            logger.info(f"Successfully translated \"{text_to_translate}\" to \"{translation}\" "
                        f"from \"{language_to_translate_from}\" "
                        f"to \"{language_to_translate_to}\" "
                        f"using {translation_service}")
            break
        else:
            logger.warning(f"Couldn't translate {text_to_translate} from {language_to_translate_from} "
                           f"to {language_to_translate_to} using any service")
            raise TranslatorError("All the specified translation services errored out")

        return translation
