import os
import re
import glob
import yaml
import subprocess
from datetime import datetime
from jinja2 import Template

def parse_note(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    fields = dict(re.findall(r'^(\w[\w\s]*?):\s*(.*?)$', content, re.MULTILINE))
    fields = {k.strip(): v.strip() for k, v in fields.items()}
    fields['Keywords'] = [kw.strip().lower() for kw in fields.get('Keywords', '').split(',')]
    return fields

def load_config(path="config.yaml"):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def filter_notes(notes, required_keywords):
    filtered = []
    for note in notes:
        if all(kw.lower() in note['Keywords'] for kw in required_keywords):
            filtered.append(note)
    return sorted(filtered, key=lambda x: int(x.get('Year', 0)))

def render_latex(entries, template_path, mode):
    with open(template_path, 'r', encoding='utf-8') as f:
        template_text = f.read()

    entry_template_text = re.search(r'% START_ENTRIES(.*?)% END_ENTRIES', template_text, re.DOTALL).group(1)
    entry_template = Template(entry_template_text)

    filled_entries = []
    for idx, entry in enumerate(entries, start=1):
        entry['index'] = idx
        filled_entries.append(entry_template.render(**entry))

    final_text = re.sub(
        r'% START_ENTRIES.*?% END_ENTRIES',
        "% START_ENTRIES\n" + "\n".join(filled_entries) + "\n% END_ENTRIES",
        template_text,
        flags=re.DOTALL
    )

    tex_filename = f"filtered_notes_{mode}.tex"
    with open(tex_filename, 'w', encoding='utf-8') as f:
        f.write(final_text)

    return tex_filename

def compile_latex(tex_file):
    subprocess.run(["pdflatex", tex_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pdf_name = tex_file.replace('.tex', '.pdf')
    print(f"✅ PDF generated: {pdf_name}")

def main():
    config = load_config()
    keyword_filter = config.get('keywords', [])
    export_mode = config.get('export_mode', 'full')  # 'full' or 'simple'

    print(f"🔍 Searching for keywords: {keyword_filter}")
    print(f"📝 Export mode: {export_mode}")

    notes_dir = "notes"
    all_notes = [parse_note(f) for f in glob.glob(os.path.join(notes_dir, '*.txt'))]
    filtered_notes = filter_notes(all_notes, keyword_filter)

    if not filtered_notes:
        print("⚠️ No notes matched the keywords.")
        return

    template_file = f"templates/{export_mode}_template.tex"
    tex_file = render_latex(filtered_notes, template_file, export_mode)
    compile_latex(tex_file)

if __name__ == "__main__":
    main()
