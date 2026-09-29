from __future__ import annotations

import html
import math
import random
import re
from dataclasses import dataclass
from typing import Iterable, List, Sequence

# -----------------------------------------------------------------------------
# common_words MUST stay present and explicit (as requested)
# Enriched FR + EN (US/UK) frequent words for lightweight Zipf-like filtering.
# -----------------------------------------------------------------------------
common_words = set([
    # French very common words
    "a", "abord", "afin", "ah", "ai", "aie", "aient", "aies", "ailleurs", "ainsi", "ait", "allaient",
    "allo", "allons", "apres", "après", "as", "assez", "attendu", "au", "aucun", "aucune", "aujourd", "aujourd'hui",
    "aupres", "auprès", "auquel", "aura", "aurait", "auraient", "aurais", "aurait", "auras", "aurez", "auriez", "aurions",
    "aurons", "auront", "aussi", "autre", "autres", "autrui", "aux", "auxquelles", "auxquels", "avaient", "avais",
    "avait", "avant", "avec", "avez", "aviez", "avions", "avoir", "avons", "ayant", "ayez", "ayons", "bah", "beaucoup",
    "bien", "bientot", "bientôt", "bon", "bonjour", "bonne", "bonnes", "bons", "bravo", "bref", "c", "ca", "car", "ce",
    "ceci", "cela", "celle", "celle-ci", "celle-là", "celles", "celles-ci", "celles-là", "celui", "celui-ci", "celui-là",
    "cent", "cependant", "certain", "certaine", "certaines", "certains", "certes", "ces", "cet", "cette", "ceux", "ceux-ci",
    "ceux-là", "chacun", "chacune", "chaque", "cher", "chere", "chère", "cheres", "chères", "chers", "chez", "chiche",
    "chut", "ci", "combien", "comme", "comment", "concernant", "contre", "couic", "crac", "d", "da", "dans", "de", "debout",
    "dedans", "dehors", "deja", "déjà", "delà", "depuis", "derriere", "derrière", "des", "desormais", "désormais", "desquelles",
    "desquels", "dessous", "dessus", "deux", "deuxieme", "deuxième", "devant", "devers", "devra", "devrait", "devraient",
    "devrais", "devrait", "devrons", "devront", "di", "different", "differente", "différente", "differentes", "différentes",
    "differents", "différents", "dire", "divers", "diverse", "diverses", "dix", "doit", "doivent", "donc", "dont", "douze",
    "du", "duquel", "durant", "e", "effet", "eh", "elle", "elle-même", "elles", "elles-mêmes", "en", "encore", "entre",
    "envers", "es", "est", "et", "etaient", "étaient", "etais", "étais", "etait", "était", "etant", "étant", "etc", "ete",
    "été", "etre", "être", "eu", "euh", "eux", "eux-mêmes", "excepté", "fais", "faisaient", "faisant", "fait", "faites", "façon",
    "fera", "ferai", "feraient", "ferais", "ferait", "feras", "ferez", "feriez", "ferions", "ferons", "feront", "fi", "flac",
    "floc", "font", "force", "furent", "fus", "fut", "g", "gens", "ha", "hein", "hem", "hep", "hi", "ho", "holà", "hop",
    "hormis", "hors", "hou", "houp", "hue", "hui", "huit", "hum", "hurrah", "i", "ici", "il", "ils", "importe", "j", "je",
    "jusqu", "jusque", "juste", "k", "l", "la", "laisser", "laquelle", "las", "le", "lequel", "les", "lesquelles", "lesquels",
    "leur", "leurs", "longtemps", "lors", "lorsque", "lui", "lui-même", "m", "ma", "maint", "mais", "malgre", "malgré", "me",
    "meme", "même", "mes", "mien", "mienne", "miennes", "miens", "mille", "mince", "moi", "moi-même", "moins", "mon", "moyennant",
    "n", "na", "ne", "neanmoins", "néanmoins", "neuf", "ni", "non", "nos", "notre", "nous", "nous-mêmes", "nul", "o", "ô", "oh",
    "ohé", "olé", "ollé", "on", "ont", "onze", "ore", "où", "ou", "ouf", "ouias", "oui", "outre", "p", "paf", "pan", "par",
    "parce", "parfois", "parle", "parlent", "parler", "parmi", "partant", "pas", "passé", "pendant", "personne", "peu", "peut",
    "peuvent", "peux", "pff", "pfft", "pfut", "pif", "plein", "plouf", "plus", "plusieurs", "plutot", "plutôt", "pouah", "pour",
    "pourquoi", "premier", "premiere", "première", "près", "proche", "psitt", "puis", "puisque", "q", "qu", "quand", "quant", "quanta",
    "quarante", "quasi", "quatorze", "quatre", "quatre-vingt", "que", "quel", "quelle", "quelles", "quelqu", "quelque", "quelques",
    "quelquun", "quelqu'une", "quelqu'un", "quels", "qui", "quiconque", "quinze", "quoi", "quoique", "r", "revoici", "revoilà", "rien",
    "s", "sa", "sacrebleu", "sans", "sapristi", "sauf", "se", "sein", "seize", "selon", "sept", "sera", "serai", "seraient", "serais",
    "serait", "seras", "serez", "seriez", "serions", "serons", "seront", "ses", "si", "sien", "sienne", "siennes", "siens", "sinon",
    "six", "soi", "soi-même", "soit", "soixante", "sommes", "son", "sont", "sous", "stop", "suis", "suivant", "sur", "surtout", "t",
    "ta", "tac", "tant", "te", "tel", "telle", "tellement", "telles", "tels", "tenant", "tes", "tic", "tien", "tienne", "tiennes", "tiens",
    "toc", "toi", "toi-même", "ton", "touchant", "toujours", "tous", "tout", "toute", "toutes", "treize", "trente", "tres", "très", "trois",
    "trop", "tu", "u", "un", "une", "va", "vais", "vas", "vers", "via", "vif", "vifs", "vingt", "vive", "vives", "vlan", "voici", "voilà",
    "vont", "vos", "votre", "vous", "vous-mêmes", "vu", "w", "x", "y", "z", "zut",

    # English common words (US + UK variants)
    "a", "about", "above", "across", "after", "afterwards", "again", "against", "ago", "ahead", "ain", "all", "almost", "alone", "along",
    "already", "also", "although", "always", "am", "among", "amongst", "an", "and", "another", "any", "anybody", "anyhow", "anyone",
    "anything", "anyway", "anywhere", "are", "aren", "around", "as", "aside", "ask", "asked", "asking", "asks", "at", "away", "back",
    "backward", "backwards", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin",
    "begins", "behind", "being", "below", "beneath", "beside", "besides", "best", "better", "between", "beyond", "both", "brief", "but",
    "by", "came", "can", "cannot", "cant", "caption", "cause", "causes", "certain", "certainly", "change", "changes", "clearly", "co", "come",
    "comes", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "could", "couldn", "course", "currently",
    "dare", "daren", "day", "de", "definitely", "despite", "did", "didn", "different", "do", "does", "doesn", "doing", "done", "don", "down",
    "downward", "downwards", "during", "each", "early", "either", "else", "elsewhere", "enough", "entirely", "especially", "et", "etc", "even",
    "ever", "every", "everybody", "everyone", "everything", "everywhere", "except", "fairly", "far", "few", "fewer", "fifth", "first", "five",
    "followed", "following", "follows", "for", "former", "formerly", "forth", "four", "from", "further", "furthermore", "gave", "get", "gets",
    "getting", "give", "given", "gives", "go", "goes", "going", "gone", "good", "got", "great", "had", "hadn", "half", "hardly", "has",
    "hasn", "have", "haven", "having", "he", "hed", "hell", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "heres",
    "hereupon", "hers", "herself", "hes", "hi", "him", "himself", "his", "hither", "hopefully", "how", "howbeit", "however", "hundred", "i",
    "id", "ie", "if", "ill", "im", "immediate", "in", "inasmuch", "inc", "indeed", "indicate", "indicated", "indicates", "inner", "inside",
    "instead", "into", "inward", "is", "isn", "it", "itd", "itll", "its", "itself", "ive", "just", "keep", "keeps", "kept", "kind", "knew",
    "know", "known", "knows", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked", "likely",
    "little", "look", "looking", "looks", "ltd", "made", "mainly", "make", "makes", "many", "may", "maybe", "mayn", "me", "mean", "meantime",
    "meanwhile", "might", "mightn", "mine", "minus", "miss", "more", "moreover", "most", "mostly", "mr", "mrs", "much", "must", "mustn",
    "my", "myself", "name", "namely", "nd", "near", "nearly", "necessary", "need", "needn", "neither", "never", "nevertheless", "new", "next",
    "nine", "ninety", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "not", "nothing", "notwithstanding", "novel",
    "now", "nowhere", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "on", "once", "one", "ones", "only", "onto", "opposite",
    "or", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "own", "particular", "particularly",
    "past", "per", "perhaps", "placed", "please", "plus", "possible", "presumably", "probably", "provided", "provides", "put", "puts", "quite", "rather",
    "really", "recent", "recently", "regarding", "regardless", "relatively", "respectively", "right", "round", "said", "same", "saw", "say", "saying", "says",
    "second", "secondly", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously",
    "seven", "several", "shall", "shan", "she", "shed", "shell", "shes", "should", "shouldn", "since", "six", "so", "some", "somebody", "someday",
    "somehow", "someone", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specified", "specify", "specifying", "still", "sub",
    "such", "sup", "sure", "take", "taken", "taking", "tell", "tends", "than", "thank", "thanks", "thanx", "that", "thatll", "thats", "thatve",
    "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "therell",
    "theres", "thereupon", "thereve", "these", "they", "theyd", "theyll", "theyre", "theyve", "thing", "things", "think", "third", "thirty", "this",
    "thorough", "thoroughly", "those", "though", "three", "through", "throughout", "thru", "thus", "till", "to", "together", "too", "took", "top", "toward",
    "towards", "tried", "tries", "truly", "try", "trying", "twelve", "twenty", "twice", "two", "under", "underneath", "undoing", "unfortunately", "unless",
    "unlike", "unlikely", "until", "unto", "up", "upon", "upward", "upwards", "us", "use", "used", "useful", "uses", "using", "usually", "value", "various",
    "very", "via", "viz", "vs", "want", "wants", "was", "wasn", "way", "we", "wed", "well", "well", "went", "were", "weren", "weve", "what", "whatever",
    "whatll", "whats", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "whereupon", "wherever", "whether", "which",
    "while", "whilst", "whither", "who", "whod", "whoever", "whole", "wholl", "whom", "whomever", "whos", "whose", "why", "will", "willing", "with",
    "within", "without", "won", "wonder", "would", "wouldn", "yes", "yet", "you", "youd", "youll", "your", "youre", "yours", "yourself", "yourselves", "youve",

    # US/UK orthographic variants and frequent educational words
    "analyze", "analyse", "analyzed", "analysed", "analyzing", "analysing", "behavior", "behaviour", "center", "centre", "color", "colour",
    "customize", "customise", "defense", "defence", "dialog", "dialogue", "enroll", "enrol", "favorite", "favourite", "fiber", "fibre", "gray", "grey",
    "honor", "honour", "learned", "learnt", "license", "licence", "modeling", "modelling", "organize", "organise", "practice", "practise", "program", "programme",
    "realize", "realise", "recognize", "recognise", "summarize", "summarise", "theater", "theatre", "traveling", "travelling", "traveled", "travelled",
    "catalog", "catalogue", "check", "checks", "checked", "checking", "reading", "reader", "readers", "school", "teacher", "teachers", "student", "students",
    "learning", "lesson", "lessons", "text", "texts", "word", "words", "sentence", "sentences", "paragraph", "paragraphs", "simple", "simpler", "easier",
    "difficult", "difficulty", "dyslexia", "dyslexic", "focus", "focused", "attention", "memory", "understand", "understanding", "comprehension", "speed", "fluency",
])

WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ'’\-]+")
VOWELS = "aeiouyàâäæéèêëîïôœùûüÿ"


@dataclass
class Analysis:
    language: str
    flesch_score: float
    asl: float
    asw: float
    zipf_common_ratio: float
    total_words: int
    common_words_count: int


@dataclass
class FormatResult:
    plain_text: str
    markdown_text: str
    html_text: str
    analysis: Analysis


def _normalize_token(token: str) -> str:
    token = token.lower().strip("'’-")
    token = token.replace("’", "'")
    return token


def tokenize_words(text: str) -> List[str]:
    return WORD_RE.findall(text)


def count_syllables(word: str) -> int:
    cleaned = re.sub(r"[^a-zàâäæéèêëîïôœùûüÿ]", "", word.lower())
    if not cleaned:
        return 1
    groups = re.findall(r"[aeiouyàâäæéèêëîïôœùûüÿ]+", cleaned)
    return max(1, len(groups))


def detect_language(text: str) -> str:
    words = [
        _normalize_token(w)
        for w in tokenize_words(text)
    ]
    if not words:
        return "fr"

    fr_markers = {
        "le", "la", "les", "des", "que", "qui", "dans", "pour", "avec", "une", "est", "pas", "vous", "nous", "sur"
    }
    en_markers = {
        "the", "and", "that", "with", "for", "you", "your", "this", "from", "have", "are", "was", "were", "they", "their"
    }

    fr_count = sum(1 for w in words if w in fr_markers)
    en_count = sum(1 for w in words if w in en_markers)
    return "en" if en_count > fr_count else "fr"


def flesch_reading_ease(text: str, language: str = "auto") -> tuple[float, float, float]:
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    words = tokenize_words(text)

    word_count = max(1, len(words))
    sentence_count = max(1, len(sentences))
    syllable_count = sum(count_syllables(word) for word in words)

    asl = word_count / sentence_count
    asw = syllable_count / word_count

    lang = detect_language(text) if language == "auto" else language
    if lang == "fr":
        # Adaptation commonly used for French readability variants
        score = 207.0 - 1.015 * asl - 73.6 * asw
    else:
        # Original Flesch Reading Ease (English)
        score = 206.835 - 1.015 * asl - 84.6 * asw

    return round(score, 2), asl, asw


def zipf_common_ratio(text: str, allowed_words: Iterable[str] = common_words) -> tuple[float, int, int]:
    tokens = [_normalize_token(t) for t in tokenize_words(text)]
    if not tokens:
        return 1.0, 0, 0

    allowed = set(allowed_words)
    common = sum(1 for t in tokens if t in allowed)
    ratio = common / len(tokens)
    return ratio, common, len(tokens)


def split_word_syllables(word: str) -> List[str]:
    # Simple language-agnostic heuristic: split around vowel/consonant transitions.
    # Keeps punctuation out (processed separately).
    letters = list(word)
    if len(letters) <= 3:
        return [word]

    chunks: List[str] = []
    current = letters[0]

    def is_vowel(ch: str) -> bool:
        return ch.lower() in VOWELS

    for idx in range(1, len(letters)):
        prev = letters[idx - 1]
        curr = letters[idx]
        nxt = letters[idx + 1] if idx + 1 < len(letters) else ""

        boundary = False
        if is_vowel(prev) and not is_vowel(curr):
            if nxt and is_vowel(nxt):
                boundary = True
        elif not is_vowel(prev) and is_vowel(curr):
            if len(current) >= 2:
                boundary = True

        if boundary:
            chunks.append(current)
            current = curr
        else:
            current += curr

    chunks.append(current)
    return [c for c in chunks if c]


def _brownian_block_sizes(
    total_syllables: int,
    rng: random.Random,
    b_min: int = 4,
    b_max: int = 11,
    b0: int = 7,
    sigma: float = 1.3,
) -> List[int]:
    if total_syllables <= 0:
        return []

    def clamp(value: int) -> int:
        return max(b_min, min(b_max, value))

    sizes: List[int] = []
    current = clamp(b0)
    consumed = 0

    while consumed < total_syllables:
        remaining = total_syllables - consumed
        if remaining <= b_max:
            sizes.append(max(1, remaining))
            break

        size = min(current, remaining)
        sizes.append(size)
        consumed += size

        epsilon = int(round(rng.gauss(0.0, sigma)))
        current = clamp(current + epsilon)

    return sizes


def _gaussian_weight(u: float, sigma_left: float, sigma_right: float) -> float:
    sigma = sigma_right if u >= 0 else sigma_left
    return math.exp(-((u * u) / (2 * sigma * sigma)))


def _compute_block_map(block_sizes: Sequence[int]) -> List[int]:
    mapping: List[int] = []
    for block_id, size in enumerate(block_sizes):
        mapping.extend([block_id] * size)
    return mapping


def _syllable_entries(text: str) -> tuple[List[dict], List[str], List[int]]:
    """Build syllable list and mapping to original token positions.

    Returns:
        syllables: list of dicts with token index and syllable string
        raw_tokens: tokenized text including separators
        syll_count_per_token: count for reconstruction
    """
    raw_tokens = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ'’\-]+|\s+|[^\s]", text, flags=re.UNICODE)
    syllables: List[dict] = []
    syll_count_per_token: List[int] = [0] * len(raw_tokens)

    for idx, token in enumerate(raw_tokens):
        if WORD_RE.fullmatch(token):
            parts = split_word_syllables(token)
            if not parts:
                parts = [token]
            syll_count_per_token[idx] = len(parts)
            for p in parts:
                syllables.append({"token_idx": idx, "text": p})

    return syllables, raw_tokens, syll_count_per_token


def format_text_brownian(
    text: str,
    seed: int | None = None,
    b_min: int = 4,
    b_max: int = 11,
    b0: int = 7,
    sigma_block: float = 1.3,
    sigma_left: float = 2.4,
    sigma_right: float = 3.7,
    tau0: float = 0.14,
) -> tuple[str, str]:
    """Return markdown and html outputs with adaptive bolding.

    Implements:
    - bounded Brownian block-size walk,
    - asymmetric Gaussian weighting,
    - adaptive threshold tau_i = tau0 * B_i,
    - extra cadence rule based on 3/2 pattern tied to block size.
    """
    if not text.strip():
        return "", ""

    rng = random.Random(seed)
    syllables, raw_tokens, syll_count_per_token = _syllable_entries(text)

    if not syllables:
        escaped = html.escape(text)
        return text, f"<p>{escaped}</p>"

    total_syllables = len(syllables)
    block_sizes = _brownian_block_sizes(
        total_syllables=total_syllables,
        rng=rng,
        b_min=b_min,
        b_max=b_max,
        b0=b0,
        sigma=sigma_block,
    )

    block_map = _compute_block_map(block_sizes)
    if len(block_map) < total_syllables:
        block_map.extend([len(block_sizes) - 1] * (total_syllables - len(block_map)))

    block_start_indices: List[int] = []
    acc = 0
    for size in block_sizes:
        block_start_indices.append(acc)
        acc += size

    styled_syllables_md: List[str] = []
    styled_syllables_html: List[str] = []

    block_mean = (b_min + b_max) / 2

    for k, syll in enumerate(syllables):
        block_id = block_map[k]
        block_size = block_sizes[block_id]
        block_start = block_start_indices[block_id]

        local_pos = k - block_start
        if block_size <= 1:
            u = 0.0
        else:
            u = (2 * local_pos / (block_size - 1)) - 1

        weight = _gaussian_weight(u, sigma_left=sigma_left, sigma_right=sigma_right)

        tau_i = min(0.98, tau0 * block_size)
        cadence = 3 if block_size >= block_mean else 2
        cadence_hit = (local_pos % cadence == 0)
        center_window = abs(u) <= (0.42 if cadence == 3 else 0.52)

        make_bold = (weight > tau_i) or (cadence_hit and center_window and weight > (tau_i * 0.92))

        txt = syll["text"]
        if make_bold:
            styled_syllables_md.append(f"**{txt}**")
            styled_syllables_html.append(f"<strong>{html.escape(txt)}</strong>")
        else:
            styled_syllables_md.append(txt)
            styled_syllables_html.append(html.escape(txt))

    # Recompose token stream
    token_to_syll_md: dict[int, List[str]] = {}
    token_to_syll_html: dict[int, List[str]] = {}

    for idx, item in enumerate(syllables):
        token_idx = item["token_idx"]
        token_to_syll_md.setdefault(token_idx, []).append(styled_syllables_md[idx])
        token_to_syll_html.setdefault(token_idx, []).append(styled_syllables_html[idx])

    out_md_parts: List[str] = []
    out_html_parts: List[str] = []
    for token_idx, token in enumerate(raw_tokens):
        if syll_count_per_token[token_idx] > 0:
            out_md_parts.append("".join(token_to_syll_md[token_idx]))
            out_html_parts.append("".join(token_to_syll_html[token_idx]))
        else:
            out_md_parts.append(token)
            out_html_parts.append(html.escape(token))

    markdown_text = "".join(out_md_parts)
    html_text = "".join(out_html_parts).replace("\n", "<br>")
    return markdown_text, f"<p>{html_text}</p>"


def analyze_text(text: str) -> Analysis:
    language = detect_language(text)
    fre, asl, asw = flesch_reading_ease(text, language=language)
    zipf_ratio, common_count, total_words = zipf_common_ratio(text)
    return Analysis(
        language=language,
        flesch_score=fre,
        asl=asl,
        asw=asw,
        zipf_common_ratio=zipf_ratio,
        total_words=total_words,
        common_words_count=common_count,
    )


def gaussReformulator(
    input_text: str,
    target_min: float = 74.0,
    target_max: float = 82.0,
    seed: int | None = None,
) -> FormatResult:
    """Unified pipeline keeping original semantics + adaptive formatting.

    The previous version used random Markov regeneration that could drift semantics.
    This version preserves user text and applies readability-aware formatting.
    """
    analysis = analyze_text(input_text)

    # Readability-aware tuning of block center to stay around the target FRE zone.
    # Lower FRE => shorter blocks (more anchors); high FRE => slightly larger blocks.
    if analysis.flesch_score < target_min:
        b0 = 6
    elif analysis.flesch_score > target_max:
        b0 = 8
    else:
        b0 = 7

    markdown_text, html_text = format_text_brownian(
        input_text,
        seed=seed,
        b_min=4,
        b_max=11,
        b0=b0,
        sigma_block=1.3,
        sigma_left=2.4,
        sigma_right=3.7,
        tau0=0.14,
    )

    return FormatResult(
        plain_text=input_text,
        markdown_text=markdown_text,
        html_text=html_text,
        analysis=analysis,
    )
