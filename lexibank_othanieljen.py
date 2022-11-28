import pylexibank
from clldutils.path import Path
from clldutils.misc import slug


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "othanieljen"

    form_spec = pylexibank.FormSpec(
        brackets={"(": ")"}, missing_data=("", " ", "-"), 
        replacements=[("ɗɨ̀ŋvi ̀", "ɗɨ̀ŋvi"), (" ", "_")],
        strip_inside_brackets=True
    )

    def cmd_makecldf(self, args):
        data = self.raw_dir.read_csv("raw.csv", dicts=True)
        args.writer.add_sources()
        languages = args.writer.add_languages(lookup_factory="Name")

        concepts = args.writer.add_concepts(
            id_factory=lambda c: c.id.split("-")[-1] + "_" + slug(c.english), lookup_factory="Name"
        )

        for row in pylexibank.progressbar(data):
            for language, lexeme in row.items():
                if language in languages:
                    args.writer.add_forms_from_value(
                        Language_ID=languages[language],
                        Parameter_ID=concepts[row["Gloss"]],
                        Value=lexeme,
                        Source="Othaniel2017",
                    )
