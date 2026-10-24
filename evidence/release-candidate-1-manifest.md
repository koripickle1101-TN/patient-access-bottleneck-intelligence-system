# PABIS Release Candidate 1 — upload manifest

Status: **LOCAL FILE VERIFIED; BINARY NOT YET UPLOADED**. No production publication authorized.

- Local filename: `Patient_Access_Bottleneck_Synthetic_Event_Control_Test_2026-10-24.xlsx`
- SHA-256: `ad4ffa5b49ff4cd85c3c0f99f234355086f1c8057871d48525397dd3bb546b85`
- Size: approximately 32 KiB (verify exact byte count on upload).
- Destination branch: `portfolio-evidence-audit-2026-10`
- Recommended destination path: `releases/Patient_Access_Bottleneck_Synthetic_Event_Control_Test_2026-10-24.xlsx`
- Keep existing workbook unchanged until a separate approved replacement decision.

## Required verification after binary upload
1. Download the file from the **review branch**, not `main`.
2. Compute its SHA-256 and compare with the manifest above. Reject any mismatch.
3. Open in Excel and inspect all source and audit worksheets, formulas, dashboard values and scenario labels.
4. Confirm 12 fictional cases, 5 Open, 5 In Progress, 2 Closed, 10 unresolved overdue and 5 source escalation flags for the fixed 2026-10-24 snapshot.
5. Verify PA-012 remains In Progress, PA-006 and PA-007 remain uncertified closures, and synthetic event scenarios do not imply real action outcomes.
6. Obtain explicit approval before merging, replacing the existing public workbook, or publishing.

## Important limits
Synthetic test records show intended safeguards only. No real patient events, employer operations, independently verified follow-up actions, or independently certified control outcomes are established.
