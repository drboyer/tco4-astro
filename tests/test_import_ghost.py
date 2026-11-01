import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ghost_import', ROOT / 'scripts/import_ghost.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'scripts').mkdir()
        for name in ['ghost-export.json', 'archive-repairs.json']:
            shutil.copyfile(ROOT / 'scripts' / name, self.root / 'scripts' / name)
        # Generate matching articles and state in isolation, independent of live edits.
        self.run_import()

    def run_import(self, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            module.import_posts(self.root, **kwargs)

    def test_idempotent_and_preserves_new_posts(self):
        post = self.root / 'src/content/blog/new-writing.md'
        post.write_text('Local writing must survive an archive import.\n')
        self.run_import()
        first = {p.name: p.read_bytes() for p in (self.root / 'src/content/blog').glob('*.md')}
        self.run_import()
        self.assertEqual(first, {p.name: p.read_bytes() for p in (self.root / 'src/content/blog').glob('*.md')})
        self.assertEqual(post.read_text(), 'Local writing must survive an archive import.\n')

    def test_local_edits_abort_before_any_writes(self):
        post = self.root / 'src/content/blog/untitled.md'
        post.write_text(post.read_text() + '\nEditorial work in progress.\n')
        before = {p.name: p.read_bytes() for p in (self.root / 'src/content/blog').glob('*.md')}
        with self.assertRaisesRegex(ValueError, r'Local changes in .*untitled\.md'):
            self.run_import()
        self.assertEqual(before, {p.name: p.read_bytes() for p in (self.root / 'src/content/blog').glob('*.md')})

    def test_stale_repair_aborts_without_writes(self):
        path = self.root / 'scripts/archive-repairs.json'
        repairs = json.loads(path.read_text())
        next(iter(repairs.values()))[0]['old'] = 'Unmatched old body'
        path.write_text(json.dumps(repairs))
        before = (self.root / 'scripts/import-state.json').read_bytes()
        with self.assertRaisesRegex(ValueError, 'Repair no longer matches'):
            self.run_import()
        self.assertEqual(before, (self.root / 'scripts/import-state.json').read_bytes())

    def test_drafts_not_imported_and_original_dates_preserved(self):
        path = self.root / 'scripts/ghost-export.json'
        export = json.loads(path.read_text())
        posts = export['db'][0]['data']['posts']
        draft = dict(posts[0], slug='private-test-draft', status='draft')
        posts.append(draft)
        path.write_text(json.dumps(export))
        self.run_import()
        self.assertFalse((self.root / 'src/content/blog/private-test-draft.md').exists())
        for post in posts[:-1]:
            output = (self.root / 'src/content/blog' / f"{post['slug']}.md").read_text()
            self.assertIn(f'pubDate: "{post["published_at"][:10]}"', output)
            self.assertNotIn('<script', output)

    def test_source_export_has_only_public_content(self):
        data = json.loads((ROOT / 'scripts/ghost-export.json').read_text())['db'][0]['data']
        self.assertEqual(set(data), {'posts', 'tags', 'posts_tags'})
        self.assertEqual(len(data['posts']), 21)
        for post in data['posts']:
            self.assertEqual(post['status'], 'published')
            self.assertLessEqual(set(post), {'id', 'title', 'slug', 'status', 'page', 'published_at', 'markdown', 'html', 'image'})

    def test_description_retains_link_labels(self):
        self.assertEqual(module.description('Read [the source](https://example.org) ![image](/image.png).'), 'Read the source .')


if __name__ == '__main__':
    unittest.main()
