import tqdm
import tskit
from IPython.core.display import HTML
from jupyterquiz import display_quiz


class DownloadProgressBar(tqdm.tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


class Workbook:
    css = """<style>
        dl {border: green 1px solid; margin-top: 1em}
        dt {color: white; background-color: green; padding: 4px; display: block; }
        dd {padding: 4px;}
    </style>"""

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

    # some useful functions
    @staticmethod
    def convert_metadata_to_new_format(ts):
        # Quick hack to read individual and population metadata as a python dict
        tables = ts.dump_tables()
        tables.populations.metadata_schema = tskit.MetadataSchema.permissive_json()
        tables.individuals.metadata_schema = tskit.MetadataSchema.permissive_json()
        tables.sites.metadata_schema = tskit.MetadataSchema.permissive_json()
        return tables.tree_sequence()

    @staticmethod
    def download(url):
        return DownloadProgressBar(
            unit="B", unit_scale=True, miniters=1, desc=url.split("/")[-1]
        )

    @property
    def setup(self):
        return HTML(self.css + self.ready_text + self.reset_button)


class WrightFisher(Workbook):
    def __init__(self):
        pass

    def Q1(self):
        display_quiz(
            [
                {
                    "question": "How many edges in this tree sequence?",
                    "type": "numeric",
                    "answers": [
                        {
                            "type": "value",
                            "value": 10,
                            "correct": True,
                            "feedback": "Correct.",
                        },
                        {
                            "type": "range",
                            "range": [-100000000, 100000],
                            "correct": False,
                            "feedback": "Try again (hint: look at `ts.num_edges()`)",
                        },
                    ],
                },
                {
                    "question": "How many sites in this tree sequence?",
                    "type": "numeric",
                    "answers": [
                        {
                            "type": "value",
                            "value": 10,
                            "correct": True,
                            "feedback": "Correct.",
                        },
                        {
                            "type": "range",
                            "range": [-100000000, 100000],
                            "correct": False,
                            "feedback": "Try again (hint: look at `ts.num_sites()`)",
                        },
                    ],
                },
                {
                    "question": "How many mutations in this tree sequence?",
                    "type": "numeric",
                    "answers": [
                        {
                            "type": "value",
                            "value": 10,
                            "correct": True,
                            "feedback": "Correct: there may be more mutations than "
                            "sites because there could be multiple mutations at a "
                            "single site",
                        },
                        {
                            "type": "range",
                            "range": [-100000000, 100000],
                            "correct": False,
                            "feedback": "Try again (hint: look at "
                            "`ts.num_mutations()`)",
                        },
                    ],
                },
            ]
        )


def setup_wright_fisher():
    return WrightFisher()
