# RUMBA.RD — reading layout and text emphasis

**A transparent text-formatting engine for reading experiments.** RUMBA.RD adds typographic emphasis while retaining the input text. It includes a browser application, a Python desktop application with document exports, and a Wix Velo port. The project is part of [Pragma Learning Institute](https://pragmalearninginstitute.com/).

[Use RUMBA.RD online](https://pragmalearninginstitute.com/rumba-rd) · [Guide français](docs/getting-started.fr.md) · [Algorithm explained](docs/algorithm.fr.md) · [PLI documentation](https://pragmalearninginstitute.com/outils/documentation)

## Start in a browser

```bash
git clone https://github.com/PragmaLearningInstitute/rumba-rd.git
cd rumba-rd
python3 -m http.server 8080 --bind 127.0.0.1 --directory web
```

Open `http://127.0.0.1:8080/rumba-rd-light.html`, paste a sample text and apply formatting. A server is needed for JavaScript modules; opening the HTML with `file://` is insufficient. HTML export is local. Other export formats may fetch browser libraries from third-party CDNs. Telemetry is disabled by default.

## Python desktop application

Python 3.11+ and a working Tk installation are recommended. Check Tk with `python3 -m tkinter`.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r desktop/requirements.txt
python desktop/app.py
```

On Windows, use `py -3 -m venv .venv`, then `.venv\Scripts\activate`. Font availability changes the layout: fonts are selected from the system, not distributed here.

## Read and reuse the code

| Component | Source | Purpose |
| --- | --- | --- |
| Python engine | `desktop/Function.py` | Analysis, approximate syllables, bounded block variation and emphasis |
| Desktop interface | `desktop/app.py`, `desktop/formatter.py` | Editing, layout and DOCX/PDF/HTML export |
| Browser engine | `web/rumbaEngine.js` | JavaScript implementation |
| Browser export | `web/rumbaExporter.js` | Export helpers |
| Wix port | `desktop/wix_velo/` | Backend function, public modules and page integration |
| Research companion | [Reading toolkit](https://github.com/PragmaLearningInstitute/reading-eye-tracking-toolkit) | Experimental protocol and exploratory gaze metrics |

[Getting started](docs/getting-started.fr.md) covers installation, exports and troubleshooting. [How the algorithm works](docs/algorithm.fr.md) explains each step and what its metrics mean. [Reproducibility and evaluation](docs/evaluation.fr.md) explains controlled comparisons, seeds, fonts and limitations. [Provenance](docs/provenance.fr.md) describes the scope of this publication.

## What this software does—and what its scores mean

The engine formats existing text; it does not use a language model to rewrite or simplify it. Its Flesch score describes the input. Adding emphasis does not demonstrate an improvement in that score or in reading comprehension. `zipf_common_ratio` is a ratio of words found in a built-in vocabulary, not an estimated Zipf frequency distribution. The tool is not a diagnostic instrument or a demonstrated treatment for dyslexia.

The Python and JavaScript versions use different random generators. A seed makes a run reproducible within its implementation; it does not promise identical output across languages.

## Tests, license and citation

```bash
python -m pip install -r desktop/requirements-dev.txt
python -m pytest desktop/tests
npm test
```

The source and original guides use the [MIT license](LICENSE). See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), [VALIDATION.md](VALIDATION.md) and [CITATION.cff](CITATION.cff). Related project: [RUMBA.EX](https://github.com/PragmaLearningInstitute/rumba-ex), for exercise recommendation.
