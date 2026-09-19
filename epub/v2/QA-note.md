# EPUB production proof v2 — QA note

**File:** `the-smallest-waiting-room-v2.epub` · **5,807 bytes** · **3 chapters / 517 story words**. Checked 19 September 2026.

The Smallest Waiting Room is original AI-assisted fiction created solely as a production demonstration. No client manuscript, personal biography, or private material was used. It is not prior client work.

## Change from the original

V2 fixes duplicate numbering in the displayed contents and explicitly hides the landmarks navigation with CSS. The story, title page, chapter documents, and navigation destinations are unchanged. The package version remains `3.0`. The original binary and its evidence were preserved separately.

## Verified

- **Official EPUBCheck 5.4.0: PASS.** Exit code 0; zero fatal errors, errors, warnings, or informational messages. Evidence: `epubcheck-report.json` and `epubcheck-output.txt`.
- **Structural checks: PASS.** ZIP integrity, required mimetype placement, XML, container, metadata, manifest, spine, navigation, and all 12 content/style links and fragments. Evidence: `structural-checks.json`.
- **Rendered content: PASS in PyMuPDF/MuPDF 1.28.2** at 390 × 700 and 768 × 1024 layout units. Both produce five pages. All 2,678 normalized visible source characters match the rendered text exactly. Only the deliberately hidden landmarks block, containing 38 normalized characters, is excluded. Numbers and punctuation are retained in the comparison.
- **Visual review: PASS for these two layouts.** All ten page images were inspected. Contents numbering is single, landmarks are hidden, and title/chapter text is legible without visible clipping or overlap. No text spans extend beyond page bounds. All four navigation labels and their page ranges were checked.

The render reports and reviewed image hashes are retained with the local QA evidence. The revision check also confirms that archive changes are limited to navigation CSS, the landmarks CSS class, and the modification timestamp.

## Limits

MuPDF still emits `unknown epub version: 3.0`; the warning is preserved. EPUBCheck reports no issues. This sample has been inspected in one rendering engine at two sizes, not on physical devices or in Kindle/Kobo applications. It is not accessibility certification, screen-reader validation, retailer acceptance, or a guarantee across reading systems. The companion HTML preview is not an EPUB reader.

SHA-256:

`7b0d58532ba1142495ec5b887d937a66b1f70b63f374dd5b7859dc427779a264`

Source, build script, and detailed evidence are retained for review. The render checker is pinned to this binary's hash; rebuilding updates the modification timestamp and requires fresh validation.
