# Dafang Zhao — personal academic website

Live website: **https://jacobzhao.github.io/**

A responsive, accessible academic website inspired by the sidebar-and-content layout of [Lingwei Zhu's homepage](https://lingweizhu.github.io/), with original HTML and CSS. Includes a biography, research interests, preprints, selected publications, academic background, and a searchable publication index.

## Edit the website

| Content | File |
| --- | --- |
| Biography, research interests, academic background, contact | `build.py` |
| Publications and selected-paper flags | `data/publications.json` |
| Layout, typography, and colors | `assets/style.css` |
| Publication filtering | `assets/main.js` |
| Profile photo | `assets/portrait.jpg` |

After editing biography or publication data, run:

```bash
python3 build.py
```

Commit the updated source **and the generated `index.html` and `publications.html`** to `main`. GitHub Pages deploys the repository root automatically. There are no package dependencies or build steps on GitHub; `.nojekyll` tells Pages to serve the committed static files directly.

To preview locally:

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000`. All publication content remains readable with JavaScript disabled; JavaScript enhances the publication page with title/author/venue search and type/year filters.

## Add a paper

Add an object to `data/publications.json`, following the existing entries. Required fields: `id`, `title`, `authors`, `venue`, `year`, `type`, `url`, and `scholar`. Set `selected: true` to include it on the homepage. Use `journal`, `conference`, `preprint`, or `book` as the type. An optional `preprint` URL adds a second link. Keep entries ordered by year, newest first.

## Content sources

- [Google Scholar](https://scholar.google.com/citations?user=62711IsAAAAJ&hl=en): publication records and public profile photo, retrieved October 21, 2026.
- [Laboratory publication list](https://www-ise2.ist.osaka-u.ac.jp/publication/): full author names and publisher links where available.
- [Faculty directory](https://www.ist.osaka-u.ac.jp/english/researcher/detail.php?id=66): public appointment and academic email.
- [ORCID](https://orcid.org/0000-0001-8107-4260): employment and degree information.
- [Doctoral thesis record](https://hdl.handle.net/11094/89577): Ph.D. field and award year.

The publication index contains 50 records from the supplied Scholar profile. Two titles sharing arXiv identifier `2505.02439` were consolidated into one entry. Other records, including a correction and separately listed workshop records, are retained; this is not a count of distinct peer-reviewed papers. Citation counts are intentionally not cached. Author lists are abbreviated where the public source was truncated. The master's institution is based on information supplied by the site owner. No CV file was supplied, so there is no placeholder download link.

The photo is the small public Scholar portrait; replace it with a higher-resolution image of the same filename when available. Publication updates are manual and do not automatically scrape Google Scholar.
