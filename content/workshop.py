from datetime import datetime

import drawsvg as draw
import tqdm
import yaml
from IPython.core.display import HTML
from jupyterquiz import display_quiz


def load_quiz(section):
    with open("quiz.yaml", "r") as fh:
        try:
            quiz = yaml.safe_load(fh)
        except yaml.YAMLError as e:
            print(e)
    if section in quiz.keys():
        return quiz[section]
    return


scilife_colors = {
    "lime": "#a7c947",
    "lime25": "#e9f2d1",
    "lime50": "#d3e4a3",
    "lime75": "#bdd775",
    "teal": "#045c64",
    "teal25": "#c0d6d8",
    "teal50": "#82aeb2",
    "teal75": "#43858b",
    "aqua": "#4c979f",
    "aqua25": "#d2e5e7",
    "aqua50": "#a6cbcf",
    "aqua75": "#79b1b7",
    "grape": "#491f53",
    "grape25": "#d2c7d4",
    "grape50": "#a48fa9",
    "grape75": "#77577e",
    "lightgray": "#e5e5e5",
    "mediumgray": "#a6a6a6",
    "darkgray": "#3f3f3f",
    "black": "#202020",
}

color_dict = {
    "--jq-multiple-choice-bg": scilife_colors[
        "lime"
    ],  # Background for the question part of multiple-choice questions
    "--jq-mc-button-bg": scilife_colors[
        "teal25"
    ],  # Background for the buttons when not pressed
    "--jq-mc-button-border": scilife_colors["teal50"],  # Border of the buttons
    "--jq-mc-button-inset-shadow": scilife_colors[
        "teal75"
    ],  # Color of inset shadow for pressed buttons
    "--jq-many-choice-bg": scilife_colors[
        "teal25"
    ],  # Background for question part of many-choice questions
    "--jq-numeric-bg": scilife_colors[
        "lime"
    ],  # Background for question part of numeric questions
    "--jq-numeric-input-bg": scilife_colors[
        "lime75"
    ],  # Background for input area of numeric questions
    "--jq-numeric-input-label": scilife_colors[
        "lime"
    ],  # Color for input of numeric questions
    "--jq-numeric-input-shadow": scilife_colors[
        "lime75"
    ],  # Color for shadow of input area of numeric questions when selected
    "--jq-incorrect-color": scilife_colors["grape"],  # Color for incorrect answers
    "--jq-correct-color": scilife_colors["teal50"],  # Color for correct answers
    "--jq-text-color": scilife_colors["lime25"],  # Color for question text
}


class DownloadProgressBar(tqdm.tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


class Workbook:
    styles = open("./styles/custom.css", "r").read()
    css = f"<style>{styles}</style>"
    # See https://github.com/jupyterlite/jupyterlite/issues/407#issuecomment-1353088447
    ready_text = """
    <table style="width: 100%;"><tr>
    <td style="text-align: left;">Your notebook is ready to go!</td>
    <td style="text-align: right;">
      <button type="button" id="button_for_indexeddb">Clear JupyterLite local storage
      </button></td>
    </tr>
    </table>
    """

    reset_button = """
    <script>
    window.button_for_indexeddb.onclick = function(e) {
        window.indexedDB.open('JupyterLite Storage').onsuccess = function(e) {
            // There are also other tables that I'm not clearing:
            // "counters", "settings", "local-storage-detect-blob-support"
            let tables = ["checkpoints", "files"];

            let db = e.target.result;
            let t = db.transaction(tables, "readwrite");

            function clearTable(tablename) {
                let st = t.objectStore(tablename);
                st.count().onsuccess = function(e) {
                    console.log("Deleting " + e.target.result +
                    " entries from " + tablename + "...");
                    st.clear().onsuccess = function(e) {
                        console.log(tablename + " is cleared!");
                    }
                }
            }

            for (let tablename of tables) {
                clearTable(tablename);
            }
        }
    };
    </script>
    """

    # Used for making SVG formatting smaller
    small_class = "x-lab-sml"
    small_style = (
        ".x-lab-sml .sym {transform:scale(0.6)} "
        ".x-lab-sml .lab {font-size:7pt;}"  # All labels small
        ".x-lab-sml .x-axis .tick .lab {"
        "font-weight:normal;transform:rotate(90deg);text-anchor:start;dominant-baseline:central;}"  # noqa
    )

    def __init__(self):
        name = type(self).__name__
        self.quiz = load_quiz(name)

    def question(self, label):
        display_quiz(self.quiz[label], colors=color_dict)

    @staticmethod
    def download(url):
        return DownloadProgressBar(
            unit="B", unit_scale=True, miniters=1, desc=url.split("/")[-1]
        )

    @property
    def setup(self):
        return HTML(self.css + self.ready_text + self.reset_button)


class HOWTO(Workbook):
    def __init__(self):
        super().__init__()
        self.quiz["Q2"][0]["answers"][0]["value"] = datetime.today().day


class WrightFisher(Workbook):
    def __init__(self):
        super().__init__()


class CoalescentHandson(Workbook):
    def __init__(self):
        super().__init__()

    def _draw_coalescent(self):
        d = draw.Drawing(210, 210, id_prefix="coal")
        d.append(draw.Circle(10, 190, 5, fill="black", stroke="black"))
        d.append(draw.Text("1", 18, 20, 210))
        d.append(draw.Circle(70, 190, 5, fill="black", stroke="black"))
        d.append(draw.Text("2", 18, 80, 210))
        d.append(draw.Circle(130, 190, 5, fill="black", stroke="black"))
        d.append(draw.Text("3", 18, 140, 210))
        d.append(draw.Circle(200, 190, 5, fill="black", stroke="black"))
        d.append(draw.Text("4", 18, 200, 210))

        d.append(draw.Circle(40, 140, 5, fill="black", stroke="black"))
        d.append(draw.Text("5", 18, 50, 150))

        d.append(draw.Circle(90, 100, 5, fill="black", stroke="black"))
        d.append(draw.Text("6", 18, 100, 110))

        d.append(draw.Circle(130, 10, 5, fill="black", stroke="black"))
        d.append(draw.Text("7", 18, 140, 20))

        d.append(draw.Line(130, 10, 90, 100, stroke="black"))
        d.append(draw.Line(130, 10, 200, 190, stroke="black"))
        d.append(draw.Line(90, 100, 130, 190, stroke="black"))
        d.append(draw.Line(90, 100, 40, 140, stroke="black"))
        d.append(draw.Line(40, 140, 70, 190, stroke="black"))
        d.append(draw.Line(40, 140, 10, 190, stroke="black"))
        return d

    def draw(self, which):
        if which == "coalescent_tree":
            return self._draw_coalescent()


def setup_coalescent_handson():
    return CoalescentHandson()


def setup_wright_fisher():
    return WrightFisher()


def setup_howto():
    return HOWTO()
