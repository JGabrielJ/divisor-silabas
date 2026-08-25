from urllib.parse import quote

import pyphen
import requests


class DictionaryUnavailableError(RuntimeError):
    """Indicates that the dictionary service could not be consulted."""


class WordAnalyzer:
    def __init__(self, word: str) -> None:
        """Receives a single word and analyzes it in detail.

        Args:
            word (str): Contains the word provided by the user.
        """
        # Vogais, consoantes e dígrafos
        self.ALPHABET: dict[str, list[str]] = {
            "vow": [
                "a",
                "á",
                "à",
                "â",
                "ã",
                "e",
                "é",
                "ê",
                "i",
                "í",
                "o",
                "ó",
                "ô",
                "õ",
                "u",
                "ú",
            ],
            "con": [
                "b",
                "c",
                "ç",
                "d",
                "f",
                "g",
                "h",
                "j",
                "k",
                "l",
                "m",
                "n",
                "p",
                "q",
                "r",
                "s",
                "t",
                "v",
                "w",
                "x",
                "y",
                "z",
            ],
            "dig": [
                "ch",
                "lh",
                "nh",
                "rr",
                "ss",
                "sç",
                "xs",
                "sc",
                "xc",
                "gu",
                "qu",
            ],
        }

        self.word: str = word.lower().strip()
        self._hyphenator = pyphen.Pyphen(lang="pt_BR")
        self._word_exists: bool | None = None

        # Inicialização dos dados da palavra
        self.syl_list: list[str] = self._hyphenator.inserted(self.word).split("-")

    def get_syllables(self) -> str:
        """Gets the syllables of the word using local Pyphen patterns.

        Returns:
            str: Contains the syllables of the user-supplied
            word if found, otherwise an empty string.
        """
        return "-".join(self.syl_list)

    def word_exists(self) -> bool:
        """Checks whether the word has an entry in Dicionário Aberto."""
        if self._word_exists is not None:
            return self._word_exists

        url = f"https://api.dicionario-aberto.net/word/{quote(self.word, safe='')}"
        try:
            response = requests.get(
                url,
                headers={"User-Agent": "DivisorDeSilabas/2.0"},
                timeout=5,
            )
        except requests.RequestException as exc:
            raise DictionaryUnavailableError from exc

        if response.status_code == 404:
            self._word_exists = False
            return False

        try:
            response.raise_for_status()
            entries = response.json()
        except (requests.RequestException, ValueError) as exc:
            raise DictionaryUnavailableError from exc

        self._word_exists = isinstance(entries, list) and bool(entries)
        return self._word_exists

    def count_letters(self) -> dict[str, int]:
        """Counts the number of letters of the user-supplied word.

        Returns:
            dict[str,int]: Indicates the length of the user-supplied word.
        """
        v_total: int = 0
        c_total: int = 0
        word_letters: str = self.word.replace("-", "")

        # Contagem de vogais e consoantes
        for char in word_letters:
            if char in self.ALPHABET["con"]:
                c_total += 1
            if char in self.ALPHABET["vow"]:
                v_total += 1

        # Contagem total de letras
        l_total: int = len(word_letters)
        return {"l": l_total, "v": v_total, "c": c_total}

    def count_phonemes(self) -> dict[str, int | list[str]]:
        """Counts the number of phonemes of the user-supplied word.

        Returns:
            dict[str,int|list[str]]: Indicates the length of the phonemes and lists it.
        """
        digraphs: list[str] = []
        phonemes = self.count_letters()["l"]

        # Letra "h" mudo
        if self.word.startswith("h"):
            phonemes -= 1

        # Dígrafos normais
        for i, d in enumerate(self.ALPHABET["dig"]):
            if d in self.word:
                qnt = self.word.count(d)
                if i <= 6:
                    phonemes -= qnt
                    digraphs.append(d) if d not in digraphs else None
                else:
                    for n in range(qnt):
                        p = self._find_nth(self.word, d, n)
                        if self.word[p + 2] in ["e", "i"]:
                            phonemes -= 1
                            digraphs.append(d) if d not in digraphs else None

        # Dígrafos vocálicos
        for s in self.syl_list:
            if len(s) > 1 and s[-2] in self.ALPHABET["vow"] and s[-1] in ["m", "n"]:
                phonemes -= 1
                dig = f"{s[-2]}{s[-1]}"
                digraphs.append(dig) if dig not in digraphs else None

        # "x" com som de "ks"
        for v in self.ALPHABET["vow"]:
            ks = f"{v}x"
            if ks in self.word:
                qnt = self.word.count(ks)
                for n in range(qnt):
                    p = self._find_nth(self.word, ks, n)
                    if (
                        self.word[p + 2] in self.ALPHABET["vow"]
                        or self.word[p + 2] == ""
                    ):
                        phonemes += 1

        return {"ph": phonemes, "dn": len(digraphs), "dg": digraphs}

    def count_syllables(self) -> dict[str, int | str]:
        """Counts the number of syllables of the user-supplied word.

        Returns:
            dict[str,int|str]: Indicates the length of the syllables and classifies it.
        """
        s_class: str = ""
        s_total: int = len(self.syl_list)

        # Checagem da quantidade de sílabas
        match s_total:
            case 1:
                s_class = "monossílaba"
            case 2:
                s_class = "dissílaba"
            case 3:
                s_class = "trissílaba"
            case _:
                s_class = "polissílaba"

        return {"tot": s_total, "cls": s_class}

    def word_stress(self) -> dict[str, str]:
        """Classify the word based on its stressed syllable.

        Returns:
            dict[str,str]: Indicates the classification of the user-supplied word.
        """
        stress_syl: str = ""
        stress_cls: str = ""
        class_list: list[str] = ["oxítona", "paroxítona", "proparoxítona"]
        ox_terminations: list[str] = [
            "r",
            "l",
            "z",
            "x",
            "i",
            "is",
            "u",
            "us",
            "im",
            "ins",
            "um",
            "uns",
            "om",
            "ons",
        ]

        # Monossílabas
        if len(self.syl_list) == 1:
            stress_syl = "".join(self.syl_list)
            stress_cls = class_list[0]
        else:
            for i, syl in reversed(list(enumerate(self.syl_list))):
                # Palavras acentuadas
                if any(
                    v
                    for v in self.ALPHABET["vow"]
                    if v not in ["a", "e", "i", "o", "u"] and v in syl
                ):
                    stress_syl = syl
                    pos = len(self.syl_list) - i
                    stress_cls = class_list[pos - 1]
                    break

            # Palavras não acentuadas
            if not stress_cls:
                if any(self.word.endswith(t) for t in ox_terminations):
                    stress_syl = self.syl_list[-1]
                    stress_cls = class_list[0]
                else:
                    stress_syl = self.syl_list[-2]
                    stress_cls = class_list[1]

        return {"syl": stress_syl, "cls": stress_cls}

    def vowel_clusters(self) -> dict[str, int]:
        """Counts the number of vowel clusters (diphthong, triphthong and hiatus).

        Returns:
            dict[str,int]: Contains the quantity of vowel clusters.
        """
        syl = self.syl_list
        diphthong, triphthong, hiatus = 0, 0, 0

        for s in syl:
            temp = s

            # Tritongos
            for i in range(len(temp) - 2):
                if (
                    temp[i] in self.ALPHABET["vow"]
                    and temp[i + 1] in self.ALPHABET["vow"]
                    and temp[i + 2] in self.ALPHABET["vow"]
                ):
                    triphthong += 1
                    temp = temp[:i] + "###" + temp[i + 3 :]

            # Ditongos
            for j in range(len(temp) - 1):
                if (
                    temp[j] in self.ALPHABET["vow"]
                    and temp[j + 1] in self.ALPHABET["vow"]
                ):
                    diphthong += 1

        # Hiatos
        for k in range(len(syl) - 1):
            cluster = f"{syl[k][-1]}{syl[k + 1][0]}"
            if (
                cluster[0] in self.ALPHABET["vow"]
                and cluster[1] in self.ALPHABET["vow"]
            ):
                hiatus += 1

        return {
            "evn": diphthong + triphthong + hiatus,
            "evd": diphthong,
            "evt": triphthong,
            "evh": hiatus,
        }

    def consonant_clusters(self) -> dict[str, int]:
        """Counts the number of consonant clusters (perfect and imperfect).

        Returns:
            dict[str,int]: Contains the quantity of consonant clusters.
        """
        syl = self.syl_list
        perfect, imperfect = 0, 0

        # Encontros consonantais perfeitos
        for s in syl:
            for i in range(len(s) - 1):
                cluster = f"{s[i]}{s[i + 1]}"
                if (
                    cluster[0] in self.ALPHABET["con"]
                    and cluster[1] in self.ALPHABET["con"]
                    and (
                        cluster not in self.ALPHABET["dig"]
                        or (
                            cluster in ["sc", "xc"]
                            and (i + 2 >= len(s) or s[i + 2] in ["a", "o", "u"])
                        )
                    )
                ):
                    perfect += 1

        # Encontros consonantais imperfeitos
        for j in range(len(syl) - 1):
            cluster = f"{syl[j][-1]}{syl[j + 1][0]}"
            if (
                cluster[0] in self.ALPHABET["con"]
                and cluster[1] in self.ALPHABET["con"]
                and (
                    cluster not in self.ALPHABET["dig"]
                    or (
                        cluster in ["sc", "xc"]
                        and (len(syl[j + 1]) < 2 or syl[j + 1][1] in ["a", "o", "u"])
                    )
                )
            ):
                imperfect += 1

        return {"ecn": perfect + imperfect, "ecp": perfect, "eci": imperfect}

    def syllables_backwards(self) -> str:
        """Reverse the syllables of the user-supplied word.

        Returns:
            str: Contains the reversed syllables.
        """
        return "-".join(list(reversed(self.syl_list)))

    def _find_nth(self, haystack: str, needle: str, n: int) -> int:
        """Source - https://stackoverflow.com/a
        Posted by Todd Gamblin, modified by community. See post 'Timeline' for change history
        Retrieved 2025-11-11, License - CC BY-SA 4.0"""

        start = haystack.find(needle)
        while start >= 0 and n > 1:
            start = haystack.find(needle, start + len(needle))
            n -= 1
        return start
