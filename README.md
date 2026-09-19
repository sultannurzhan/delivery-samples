# Sultan Takibay - technical delivery samples

Small, original demonstrations of how I prepare and check a deliverable. These samples were created with AI assistance. They contain fictional material and are not previous client projects.

## CSV preparation with traceable exceptions

[Read the rules and results](data/README.md) · [Input](data/input.csv) · [Clean output](data/cleaned.csv) · [Exceptions](data/exceptions.csv) · [Source code](data/cleanup.py)

Ten synthetic source rows produce four clean records representing five source IDs, plus five quarantined rows. One duplicate is collapsed and no original row is unaccounted for. The checks cover conflicting values, ambiguous dates, invalid quantities and the difference between missing and zero.

The Python script uses only the standard library. Run `python data/cleanup.py` to reproduce the outputs and verification report. The rules are explicit for this small demonstration; real files require their own agreed keys, formats and acceptance criteria.

## Reflowable EPUB production

[Download the corrected EPUB v2](epub/v2/the-smallest-waiting-room-v2.epub) · [Read the original manuscript](epub/manuscript.md) · [Validation note](epub/v2/QA-note.md)

A three-chapter, 517-word original fictional sample. EPUBCheck 5.4.0 reported zero fatal errors, errors or warnings. Independent checks cover package structure, metadata, navigation and all content links. This is a technical formatting example, not an editorial portfolio or accessibility certification.

Version 2 corrects contents-list numbering and hidden-landmarks display. All ten pages passed visual review in MuPDF 1.28.2 at phone and tablet layout sizes, with exact visible-text preservation. One engine warning remains documented. Dedicated ebook-reader, screen-reader and physical-device tests have not been completed; those checks must be scoped for a real publication.

The [original v1 file](epub/the-smallest-waiting-room.epub) and [its QA record](epub/QA-note.md) are preserved.

## Working approach

Agree the input, output, acceptance checks, permitted tools and data handling before production. Preserve uncertainty instead of inventing values. Deliver a reproducible result and a concise handover.

No client code, manuscripts, credentials or personal datasets are included here. Commercial scope, price, schedule and terms are agreed separately; these examples do not establish a booking or service agreement.

## Enquire about a small paid task

[Email Sultan Takibay](mailto:takibaysultan@gmail.com) with the problem, input/output format, approximate size and desired deadline. A short description is enough initially; please keep credentials and confidential files out of the first message.

Examples of proposed pilot scopes:

- **CSV preparation — US$125:** one non-personal file, up to 500 rows and 15 columns, agreed cleanup rules, clean output, exceptions/reconciliation log, a rerunnable script and one correction round.
- **Text-only EPUB — US$60 up to 7,500 words, or US$100 up to 15,000 words:** clean English prose, linked contents, metadata, validation evidence and one correction round. Reader-specific checks and any complex content need separate scoping.
- **Software repair or technical validation:** one reproducible defect or behavior, with the deliverable and fixed price agreed after reviewing the brief. A typical API/import repair pilot is proposed at US$150.

Based in South Korea (UTC+9). AI assistance is part of this workflow and is disclosed; permitted tools and data handling are agreed for each assignment. These are proposals, not automatic bookings. Work starts only after written agreement on scope, acceptance criteria, price, deadline, revisions and payment terms.
