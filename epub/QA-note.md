# EPUB validation evidence

**File:** `the-smallest-waiting-room.epub` - 5,776 bytes; three chapters; 517 story words.

Created on 19 September 2026 from original AI-assisted fiction. This is a fresh technical demonstration, not previous client work.

- Official EPUBCheck 5.4.0: zero fatal errors, errors or warnings.
- ZIP integrity; first and uncompressed `mimetype`; XML parsing; complete manifest; spine order; navigation; all 12 content/style links and metadata passed independent structural checks.
- Reflowable EPUB3, English metadata, scalable CSS, no scripts, tracking, external resources, DRM or embedded fonts.

The SHA-256 of the checked file is:

`65a893e5723ddde4445db6d1c40eab1fa7b228e278e935ed9add9005be373bfa`

Recheck with the official [EPUBCheck 5.4.0 release](https://github.com/w3c/epubcheck/releases/tag/v5.4.0):

```text
java -jar epubcheck.jar the-smallest-waiting-room.epub
```

## Limits

This does not establish store acceptance, accessibility certification or compatibility with specific reading systems. Dedicated ebook-reader, screen-reader and cross-device tests have not been performed. Those checks need explicit scoping for a real publication.

## Additional renderer diagnostic — 19 September 2026

The unchanged EPUB was rendered with PyMuPDF/MuPDF 1.28.2 at 390×700 and 768×1024 layout sizes. All ten generated page images were inspected. The contents page shows duplicate list numbering and exposes the landmarks navigation in this engine. The engine also emits `unknown epub version: 3.0` despite the separate EPUBCheck pass. This is a known rendering limitation of this sample/engine combination, not a clean visual pass. The other page text was legible and within the page bounds.

This single-engine diagnostic does not establish physical-device compatibility, Kindle/Kobo behavior, or accessibility compliance. Resolve navigation presentation and agree target-reader testing before any production acceptance.
