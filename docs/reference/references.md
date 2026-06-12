# Event Participation Request reference

This reference describes the fields of the **Event Participation Request** entry and gives guidance for completing each part. The entry is organized into a main section (applicant and participant information) and three subsections: **event details**, **expected expenses**, and **status**.

## Applicant and participant information

These fields appear at the top of the entry.

| Field | What it is | Notes |
|---|---|---|
| **Submitter** | The person filling in the form. | Filled automatically from your logged-in account; read-only. |
| **Date** | Submission date. | Set automatically on first save; read-only. |
| **Participant: Same as submitter** | Whether the participant is the same person as the submitter. | Checked by default. Keep it checked when the request is for yourself. Uncheck it if you are filling in the form on behalf of someone else, then enter that person's details below. |
| **Participant full name (First, Last)** | Full name of the event participant. | Suggestions from the FAIRmat team list. Filled automatically when *Same as submitter* is checked. |
| **Participant email** | E-mail of the event participant. | Suggestions from the FAIRmat team list. Filled automatically when *Same as submitter* is checked. |
| **Role in FAIRmat** | The participant's role. | One of `PI`, `Coordinator`, `Coworker`, `Collaborator`. |
| **FAIRmat Area(s)** | The participant's FAIRmat area(s). | One or more of Areas A–H. |
| **Tags** | Optional free-form tags for search and categorization. | Add one or more. |
| **Notes** | Free-form notes about this request. | Optional. |
| **Summary (auto-generated)** | A generated overview of the request. | Read-only; updates when you save. |
| **Total expenses** | Sum of the expected expenses. | Read-only; calculated from the expense subsections. |
| **Generate summary PDF** | Generates a PDF summary of the request. | Check and save to produce the PDF. |

## Event details

The **event details** subsection describes the event you would like to attend.

| Field | What to enter | Example |
|---|---|---|
| **event name** | The name of the event. | `E-MRS Spring Meeting 2026` |
| **Event website** | URL of the event's website. | `https://www.european-mrs.com/` |
| **Organizer/Host** | The organizing entity or host. | `European Materials Research Society` |
| **Event location** | Where the event takes place. | `Strasbourg, France` |
| **event start date** | Start date of the event. | `2026-05-25` |
| **event end date** | End date of the event. | `2026-05-28` |
| **attendance method** | How you will attend. | `In-person`, `Virtual` |
| **participation type** | Your type of participation. | `Invited talk`, `Contributed talk/poster`, `Booth representation`, `User support, offer training, or demonstration`, `Other` |
| **title of contribution** | Title of your contribution, if any. | `FAIR data workflows in materials science` |

## Expected expenses

The **expected expenses** subsection is repeatable: add one entry per expense category. When you add an expense, choose the category from the dropdown, which determines the fields shown.

### Transportation

| Field | What to enter |
|---|---|
| **Transportation Method** | `Train`, `Flight`, `Car`, `Taxi`, `Public transport`, or `Other`. |
| **Cost (Euro)** | Estimated transportation cost. |
| **Justification** | Mandatory for 1st-class train travel, flights, taxis, or business-class tickets. |

### Accommodation

| Field | What to enter |
|---|---|
| **Number of nights** | Number of accommodation nights needed. |
| **Cost (Euro)** | Total accommodation cost. The cost per night is calculated automatically. |
| **Justification** | Mandatory when the cost is above €90/night. |

### Conference

| Field | What to enter |
|---|---|
| **Registration fees (Euro)** | Conference or event registration fee. |

### Other

| Field | What to enter |
|---|---|
| **Cost description** | A short description of the other cost. |
| **Other costs (Euro)** | The amount of the other cost. |
| **Justification** | Justification for the other cost. |

## Status

The **status** subsection is for the **Outreach and Administration admins only**. Applicants should not edit it.

| Field | What it is |
|---|---|
| **Request status** | `Under review`, `Approved`, or `Rejected`. |
| **To be paid from** | Where the expenses will be covered from: `HU` or `FAIR-DI`. |
