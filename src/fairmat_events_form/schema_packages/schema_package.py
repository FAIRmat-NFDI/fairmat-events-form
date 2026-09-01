import json
import os
from datetime import datetime
from typing import TYPE_CHECKING

from nomad.config import config
from nomad.datamodel.data import ArchiveSection, Schema, UseCaseElnCategory
from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum
from nomad.metainfo import MEnum, Quantity, SchemaPackage
from nomad.metainfo.metainfo import Datetime, Section, SubSection

if TYPE_CHECKING:
    pass

# Access plugin configuration
configuration = config.get_plugin_entry_point(
    'fairmat_events_form.schema_packages:events_schema_package_entry_point'
)

m_package = SchemaPackage()

# -----------------------------
# FAIRmat team file loading
# -----------------------------
# The team file location is a deployment concern, decoupled from the code:
#   1. FAIRMAT_TEAM_FILE env var (set by deployment, e.g. a bind-mounted host file)
#   2. module-relative fallback for local dev (repo-root fairmat_team.json)
# Missing file -> empty team list (the plugin still loads).
_DEFAULT_TEAM_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', '..', 'fairmat_team.json')
)
_TEAM_PATH = os.environ.get('FAIRMAT_TEAM_FILE', _DEFAULT_TEAM_FILE)

# Human-readable area labels, kept consistent across all FAIRmat plugins
# (fairmat-members, fairmat-onboarding, fairmat-events-form): the word 'Area',
# the letter, a ' - ' separator, then the name.
FAIRMAT_AREAS = [
    'Area A - Synthesis',
    'Area B - Experiment',
    'Area C - Computation',
    'Area D - Data modeling and interoperability',
    'Area E - Digital infrastructure',
    'Area F - Enabling data-driven science',
    'Area G - Outreach',
    'Area H - Management',
]


def _load_team():
    try:
        with open(_TEAM_PATH) as f:
            return json.load(f)
    except FileNotFoundError:
        return []


_TEAM = _load_team()
_TEAM_BY_EMAIL = {p['email'].lower(): p for p in _TEAM}
_TEAM_NAMES = [p['full_name'] for p in _TEAM]
_TEAM_EMAILS = [p['email'] for p in _TEAM]


# -----------------------------
# Define schema sections
# -----------------------------
class RequestStatus(ArchiveSection):
    """
    A subsection for updating the status of the request -
    to be used only by the Outreach and Adminstration admins.
    """

    status = Quantity(
        type=MEnum(
            'Under review',
            'Approved',
            'Rejected',
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
        description='what is the current status of the request',
        label='Request status',
    )

    reimbursement_source = Quantity(
        type=MEnum(
            'HU',
            'FAIR-DI',
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
        description='How will the event expenses be covered',
        label='To be paid from',
    )


class EventExpenses(ArchiveSection):
    """
    A subsection for providing the expected costs associated with the event.
    """

    m_def = Section(
        label='Please choose a specific expense category',
        label_quantity='name',
    )

    name = Quantity(type=str)

    intro_expenses = Quantity(
        type=str,
        label='Select one category for expenses from the dropdown menu above.',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        # Used as the item label in the sub-section list (via label_quantity)
        self.name = self.m_def.label or self.m_def.name


class TransportationExpenses(EventExpenses):
    m_def = Section(label='Transportation', label_quantity='name')

    travel_method = Quantity(
        type=MEnum('Train', 'Flight', 'Car', 'Taxi', 'Public transport', 'Other'),
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
        label='Transportation Method',
        description='Costs associated to traveling to the conference venue',
    )

    travel_cost = Quantity(
        type=float,
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
        label='Cost (Euro)',
        description='Costs associated to traveling to the event venue',
    )

    travel_justification = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        label='Justification (mandatory for 1st class train travel, flights, taxis,\
                  or business-class tickets)',
        description='Costs associated to traveling to the event venue',
    )


class AccommodationExpenses(EventExpenses):
    m_def = Section(label='Accommodation', label_quantity='name')

    accomodation_duration = Quantity(
        type=int,
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
        label='Number of nights',
        description='Number of accommodation nights needed',
    )

    accommodation_cost = Quantity(
        type=float,
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
        label='Cost (Euro)',
        description='Costs associated to traveling to the event venue',
    )

    accommodation_justification = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        label='Justification (mandatory when this cost is above €90/night)',
        description='Costs associated to traveling to the event venue',
    )

    cost_night = Quantity(type=float, label='Cost per night')

    def normalize(self, archive, logger):
        super().normalize(archive, logger)
        night = self.accomodation_duration or 1
        total_cost = self.accommodation_cost or 0
        self.cost_night = total_cost / night


class ConferenceExpenses(EventExpenses):
    m_def = Section(label='Conference fee', label_quantity='name')

    conference_cost = Quantity(
        type=float,
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
        label='Registration fees (Euro)',
        description='Costs associated to traveling to the event venue',
    )


class OtherExpenses(EventExpenses):
    m_def = Section(label='Other', label_quantity='name')

    other_expenses_description = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        label='Cost description',
        description='Other costs associated with the event',
    )
    other_cost = Quantity(
        type=float,
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
        label='Other costs (Euro)',
        description='Other costs associated with the event',
    )
    other_costs_justification = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        label='Justification',
        description='Costs associated to traveling to the event venue',
    )


class EventInformation(ArchiveSection):
    """
    An Entry for requesting an approval to attend an external event.
    """

    event_name = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description='The Name of the event',
    )

    event_website = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.URLEditQuantity),
        description='Event Website',
        label='Event website',
        default='https://',
    )

    event_organizer_or_host = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description='Name of the organizing entity or host',
        label='Organizer/Host',
    )

    location = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description='Location where the event takes place',
        label='Event location',
    )

    event_start_date = Quantity(
        type=Datetime, a_eln=ELNAnnotation(component=ELNComponentEnum.DateEditQuantity)
    )

    event_end_date = Quantity(
        type=Datetime, a_eln=ELNAnnotation(component=ELNComponentEnum.DateEditQuantity)
    )

    attendance_method = Quantity(
        type=MEnum(
            'In-person',
            'Virtual',
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
        description='Attendance method',
    )

    participation_type = Quantity(
        type=MEnum(
            'Invited talk',
            'Contributed talk/poster',
            'Booth representation',
            'User support, offer training, or demonstration',
            'Other',
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
        description='Type of participation',
    )

    title_of_contribution = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description='Title of the contribution',
    )


# Term subsection for multi-value FAIRmat area —
# same indexing pattern as nomad-training-resources
class FairmatAreaTerm(ArchiveSection):
    m_def = Section(a_eln={'hide': ['value']})
    value = Quantity(type=MEnum(*FAIRMAT_AREAS), label_quantity='value')


class ApplicantInformation(Schema):
    """
    An Entry for requesting an approval to attend an external event.
    """

    m_def = Section(
        label='Event Participation Request',
        categories=[UseCaseElnCategory],
        a_eln={
            'hide': [
                'fairmat_area_terms',
                'pdf_generated_timestamp',
            ]
        },
    )

    # --- Read-only header fields (rendered first under QUANTITIES) ---
    submitted_by = Quantity(
        type=str,
        label='Submitter',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        a_display={'editable': False},
        description=(
            'Auto-filled from the logged-in user matched against the FAIRmat team list.'
        ),
    )

    submission_date = Quantity(
        type=Datetime,
        label='Date',
        a_eln=ELNAnnotation(component=ELNComponentEnum.DateEditQuantity),
        a_display={'editable': False},
        description="Auto-filled with today's date on first save.",
    )

    # --- Participant section ---
    participant_same_as_submitter = Quantity(
        type=bool,
        default=True,
        label='Participant: Same as submitter',
        a_eln=ELNAnnotation(component=ELNComponentEnum.BoolEditQuantity),
        description=(
            'Check this if the person attending the event is the same as the '
            'person submitting this form. When checked and saved, the fields '
            'below are filled automatically.'
        ),
    )

    full_name = Quantity(
        type=str,
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            props=dict(suggestions=_TEAM_NAMES),
        ),
        description='Full name of the event participant',
        label='Participant full name (First, Last)',
    )

    email = Quantity(
        type=str,
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
            props=dict(suggestions=_TEAM_EMAILS),
        ),
        description='Email of the event participant',
        label='Participant email',
    )

    role_at_fairmat = Quantity(
        type=MEnum(
            'PI',
            'Coordinator',
            'Coworker',
            'Collaborator',
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
        description='Role of the participant in FAIRmat',
        label='Role in FAIRmat',
    )

    fairmat_areas = Quantity(
        type=MEnum(*FAIRMAT_AREAS),
        shape=['*'],
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.EnumEditQuantity,
        ),
        label='FAIRmat Area(s)',
        description='FAIRmat area(s) of the participant.',
    )

    # Repeatable free-text tags — standard NOMAD pattern (same as TrainingResource.tags)
    tags = Quantity(
        type=str,
        shape=['*'],
        label='Tags',
        description='Add one or more free-form tags for search and categorisation.',
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
    )

    # --- Editable free-text notes ---
    notes = Quantity(
        type=str,
        label='Notes',
        a_eln=ELNAnnotation(component=ELNComponentEnum.RichTextEditQuantity),
        description='Free-form notes about this event participation request.',
    )

    # --- Auto-generated rich-text summary (read-only) ---
    summary = Quantity(
        type=str,
        label='Summary (auto-generated)',
        a_eln=ELNAnnotation(component=ELNComponentEnum.RichTextEditQuantity),
        a_display={'editable': False},
        description='Auto-generated summary shown in overview',
    )

    total_expenses = Quantity(
        type=float,
        a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
        a_display={'editable': False},
        label='Total expenses',
    )

    generate_pdf = Quantity(
        type=bool,
        default=False,
        label='Generate summary PDF',
        a_eln=ELNAnnotation(component=ELNComponentEnum.BoolEditQuantity),
        description='Check to generate a PDF summary of this request.',
    )

    pdf_generated_timestamp = Quantity(
        type=Datetime,
        description='Timestamp when the PDF was generated (hidden from form).',
    )

    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        # --- Identify logged-in user from NOMAD archive metadata ---
        author = archive.metadata.main_author if archive.metadata else None
        submitter = None
        # Submitter's display name always comes from Keycloak (the logged-in user),
        # not from the team list. The team list is still used to confirm membership
        # and to provide area/role.
        submitter_name = ''
        if author:
            user_email = getattr(author, 'email', None)
            first = getattr(author, 'first_name', '') or ''
            last = getattr(author, 'last_name', '') or ''
            submitter_name = f'{first} {last}'.strip()
            logger.info(
                f'EventForm normalize: main_author email={user_email!r}, '
                f'first_name={getattr(author, "first_name", None)!r}, '
                f'last_name={getattr(author, "last_name", None)!r}'
            )
            if user_email:
                submitter = _TEAM_BY_EMAIL.get(user_email.lower())
            # Fallback: match by full name if email lookup failed
            if submitter is None:
                submitter = next(
                    (p for p in _TEAM if p['full_name'] == submitter_name), None
                )
                if submitter:
                    logger.info(
                        'EventForm normalize: matched team member by name: '
                        f'{submitter_name!r}'
                    )

        # --- Always update submitted_by (reflects logged-in user each save) ---
        if submitter:
            areas = submitter.get('fairmat_areas') or []
            area_str = areas[0] if areas else ''
            self.submitted_by = f'{submitter_name} ({area_str})'
        else:
            # Not in the FAIRmat team list — show clear warning
            self.submitted_by = (
                'Submitter is not in the FAIRmat team list. '
                'Please contact administration.'
            )

        # --- Set submission date once on first save (NOMAD-native datetime) ---
        if not self.submission_date:
            self.submission_date = datetime.utcnow()

        # --- Resolve participant from the FAIRmat team list ---
        # When checkbox is checked: use the submitter as participant.
        # When unchecked: look up by email first (authoritative), then by full_name.
        # The email always wins — if email and name disagree,
        # name is corrected from the team list.
        participant = None
        if self.participant_same_as_submitter:
            participant = submitter
        else:
            if self.email:
                participant = _TEAM_BY_EMAIL.get(self.email.strip().lower())
            if participant is None and self.full_name:
                participant = next(
                    (p for p in _TEAM if p['full_name'] == self.full_name.strip()),
                    None,
                )

        if participant:
            self.full_name = participant['full_name']
            self.email = participant['email']
            areas = participant.get('fairmat_areas') or []
            if isinstance(areas, str):
                areas = [areas]
            self.fairmat_areas = areas
            self.role_at_fairmat = participant.get('role_at_fairmat')

        # --- Sync fairmat_areas into indexed FairmatAreaTerm subsections ---
        if self.fairmat_areas:
            self.fairmat_area_terms = [
                FairmatAreaTerm(value=area) for area in self.fairmat_areas
            ]

        # --- Build header line for the summary ---
        date_str = (
            self.submission_date.strftime('%d.%m.%Y') if self.submission_date else '?'
        )
        if submitter:
            # Display name from Keycloak (the logged-in user); area from team list.
            header_name = submitter_name or '(unknown)'
            areas = submitter.get('fairmat_areas') or []
            area_short = areas[0].split(' - ')[0].removeprefix('Area ').strip() \
                if areas else '?'
        else:
            # Fallback to the author's display name even when not in the team list
            header_name = submitter_name or '(unknown)'
            area_short = '?'

        # --- Build rich-text summary ---
        details = self.event_details if hasattr(self, 'event_details') else None
        expenses = self.expected_expenses if hasattr(self, 'expected_expenses') else []
        status = self.status if hasattr(self, 'status') else None
        parts = []
        total_cost = 0.0

        parts.append(
            f'<b>Submitted by:</b> {header_name}, Area {area_short}, on {date_str}'
        )

        if self.full_name:
            parts.append(f'<b>Participant:</b> {self.full_name}')
        if self.fairmat_areas:
            parts.append(f'<b>FAIRmat Area(s):</b> {", ".join(self.fairmat_areas)}')

        if details:
            if details.event_name:
                parts.append(f'<b>Event:</b> {details.event_name}')
            if details.event_start_date and details.event_end_date:
                parts.append(
                    f'<b>Date:</b> {details.event_start_date.date()}'
                    f' – {details.event_end_date.date()}'
                )
            elif details.event_start_date:
                parts.append(f'<b>Date:</b> {details.event_start_date.date()}')
            if details.location:
                parts.append(f'<b>Location:</b> {details.location}')
            if details.participation_type:
                parts.append(f'<b>Participation:</b> {details.participation_type}')

        if expenses:
            parts.append('<b>Expected expenses</b>')
            for exp in expenses:
                expense_fields = [
                    ('travel_cost', 'Travel cost', 'travel_method'),
                    ('accommodation_cost', 'Accommodation', None),
                    ('conference_cost', 'Registration fees', None),
                    ('other_cost', 'Other costs', 'other_expenses_description'),
                ]
                for attr, field_label, note_attr in expense_fields:
                    if hasattr(exp, attr) and getattr(exp, attr):
                        value = getattr(exp, attr)
                        note = (
                            getattr(exp, note_attr)
                            if note_attr
                            and hasattr(exp, note_attr)
                            and getattr(exp, note_attr)
                            else ''
                        )
                        suffix = f' ({note})' if note else ''
                        parts.append(f'• {field_label}: €{value:.2f}{suffix}')
                        total_cost += value

        if total_cost > 0:
            parts.append(f'<b>Total expenses:</b> €{total_cost:.2f}')
            self.total_expenses = total_cost

        if status and status.status:
            parts.append(f'<b>Status:</b> {status.status}')

        self.summary = '<br>'.join(parts)

        # --- Generate PDF (server-side only, skip in client context) ---
        from nomad.datamodel.context import ClientContext

        if self.generate_pdf and not isinstance(archive.m_context, ClientContext):
            try:
                self.pdf_generated_timestamp = datetime.utcnow()
                self._write_pdf(
                    archive,
                    logger,
                    header_name,
                    area_short,
                    date_str,
                    details,
                    expenses,
                    status,
                    total_cost,
                )
            except Exception as e:
                logger.warning(f'EventForm: PDF generation failed: {e}')

    def _write_pdf(
        self,
        archive,
        logger,
        header_name,
        area_short,
        date_str,
        details,
        expenses,
        status,
        total_cost,
    ):
        from io import BytesIO

        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.platypus import (
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )

        # --- Build filename: YYYY-MM-DD_LastName_EventName.pdf ---
        date_file = (
            self.submission_date.strftime('%Y-%m-%d')
            if self.submission_date
            else 'unknown-date'
        )
        last_name = (self.full_name or 'unknown').split()[-1]
        event_name = (
            details.event_name if details and details.event_name else 'unknown-event'
        )

        # Sanitize for filesystem
        def safe(s):
            return ''.join(c if c.isalnum() or c in '-_.' else '_' for c in s)

        pdf_filename = f'{safe(date_file)}_{safe(last_name)}_{safe(event_name)}.pdf'

        buf = BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=A4,
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )
        styles = getSampleStyleSheet()
        normal = styles['Normal']
        title_style = ParagraphStyle(
            'title', parent=styles['Title'], fontSize=16, spaceAfter=12
        )
        section_style = ParagraphStyle(
            'section',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=12,
            spaceBefore=12,
            spaceAfter=4,
            textColor=colors.HexColor('#003366'),
        )

        story = []

        story.append(Paragraph('FAIRmat Event Participation Request', title_style))
        story.append(Spacer(1, 0.3 * cm))

        # --- Header table ---
        header_data = [
            [
                Paragraph('<b>Submitted by:</b>', normal),
                Paragraph(f'{header_name}, Area {area_short}', normal),
            ],
            [Paragraph('<b>Date:</b>', normal), Paragraph(date_str, normal)],
        ]
        if self.full_name:
            header_data.append(
                [
                    Paragraph('<b>Participant:</b>', normal),
                    Paragraph(self.full_name, normal),
                ]
            )
        if self.email:
            header_data.append(
                [Paragraph('<b>Email:</b>', normal), Paragraph(self.email, normal)]
            )
        if self.role_at_fairmat:
            header_data.append(
                [
                    Paragraph('<b>Role in FAIRmat:</b>', normal),
                    Paragraph(self.role_at_fairmat, normal),
                ]
            )
        if self.fairmat_areas:
            header_data.append(
                [
                    Paragraph('<b>FAIRmat Area(s):</b>', normal),
                    Paragraph(', '.join(self.fairmat_areas), normal),
                ]
            )

        header_table = Table(header_data, colWidths=[4.5 * cm, 12 * cm])
        header_table.setStyle(
            TableStyle(
                [
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ]
            )
        )
        story.append(header_table)
        story.append(Spacer(1, 0.5 * cm))

        # --- Event details ---
        if details:
            story.append(Paragraph('Event Details', section_style))
            event_data = []
            if details.event_name:
                event_data.append(
                    [
                        Paragraph('<b>Event:</b>', normal),
                        Paragraph(details.event_name, normal),
                    ]
                )
            if details.event_website and details.event_website != 'https://':
                event_data.append(
                    [
                        Paragraph('<b>Website:</b>', normal),
                        Paragraph(details.event_website, normal),
                    ]
                )
            if details.event_organizer_or_host:
                event_data.append(
                    [
                        Paragraph('<b>Organizer:</b>', normal),
                        Paragraph(details.event_organizer_or_host, normal),
                    ]
                )
            if details.location:
                event_data.append(
                    [
                        Paragraph('<b>Location:</b>', normal),
                        Paragraph(details.location, normal),
                    ]
                )
            if details.event_start_date and details.event_end_date:
                event_data.append(
                    [
                        Paragraph('<b>Dates:</b>', normal),
                        Paragraph(
                            f'{details.event_start_date.date()} – '
                            f'{details.event_end_date.date()}',
                            normal,
                        ),
                    ]
                )
            elif details.event_start_date:
                event_data.append(
                    [
                        Paragraph('<b>Date:</b>', normal),
                        Paragraph(str(details.event_start_date.date()), normal),
                    ]
                )
            if details.attendance_method:
                event_data.append(
                    [
                        Paragraph('<b>Attendance:</b>', normal),
                        Paragraph(details.attendance_method, normal),
                    ]
                )
            if details.participation_type:
                event_data.append(
                    [
                        Paragraph('<b>Participation type:</b>', normal),
                        Paragraph(details.participation_type, normal),
                    ]
                )
            if details.title_of_contribution:
                event_data.append(
                    [
                        Paragraph('<b>Contribution title:</b>', normal),
                        Paragraph(details.title_of_contribution, normal),
                    ]
                )
            if event_data:
                t = Table(event_data, colWidths=[4.5 * cm, 12 * cm])
                t.setStyle(
                    TableStyle(
                        [
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                        ]
                    )
                )
                story.append(t)
                story.append(Spacer(1, 0.5 * cm))

        # --- Expenses ---
        if expenses:
            story.append(Paragraph('Expected Expenses', section_style))
            expense_rows = [
                [
                    Paragraph('<b>Category</b>', normal),
                    Paragraph('<b>Cost (€)</b>', normal),
                    Paragraph('<b>Details</b>', normal),
                ]
            ]
            expense_map = [
                ('travel_cost', 'Travel', 'travel_method'),
                ('accommodation_cost', 'Accommodation', 'accommodation_justification'),
                ('conference_cost', 'Registration fees', None),
                ('other_cost', 'Other', 'other_expenses_description'),
            ]
            for exp in expenses:
                for attr, label, note_attr in expense_map:
                    if hasattr(exp, attr) and getattr(exp, attr):
                        val = getattr(exp, attr)
                        note = getattr(exp, note_attr, '') or '' if note_attr else ''
                        expense_rows.append(
                            [
                                Paragraph(label, normal),
                                Paragraph(f'{val:.2f}', normal),
                                Paragraph(note, normal),
                            ]
                        )
            if total_cost > 0:
                expense_rows.append(
                    [
                        Paragraph('<b>Total</b>', normal),
                        Paragraph(f'<b>{total_cost:.2f}</b>', normal),
                        Paragraph('', normal),
                    ]
                )
            t = Table(expense_rows, colWidths=[4 * cm, 3 * cm, 9.5 * cm])
            t.setStyle(
                TableStyle(
                    [
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4169E1')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ]
                )
            )
            story.append(t)
            story.append(Spacer(1, 0.5 * cm))

        # --- Status ---
        if status and status.status:
            story.append(Paragraph('Status', section_style))
            story.append(Paragraph(f'<b>Request status:</b> {status.status}', normal))
            if status.reimbursement_source:
                story.append(
                    Paragraph(
                        f'<b>To be paid from:</b> {status.reimbursement_source}', normal
                    )
                )

        # --- Footer with timestamp (small text) ---
        story.append(Spacer(1, 1 * cm))
        timestamp_text = (
            self.pdf_generated_timestamp.strftime('%d.%m.%Y %H:%M')
            if self.pdf_generated_timestamp
            else 'N/A'
        )
        footer_style = ParagraphStyle(
            'footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#666666'),
            alignment=1,
        )
        story.append(
            Paragraph(f'Summary PDF generated at {timestamp_text}', footer_style)
        )

        doc.build(story)

        with archive.m_context.raw_file(pdf_filename, 'wb') as f:
            f.write(buf.getvalue())
        logger.info(f'EventForm: PDF written as {pdf_filename}')

    event_details = SubSection(
        section_def=EventInformation,
        description='',
        repeats=False,
    )

    expected_expenses = SubSection(
        section_def='EventExpenses',
        description='',
        repeats=True,
    )

    status = SubSection(
        section_def='RequestStatus',
        label='Status - To be filled only by Outreach and Adminstration admins',
        description='',
        repeats=False,
    )

    # Hidden subsection — stores indexed, searchable FAIRmat area terms
    fairmat_area_terms = SubSection(section_def=FairmatAreaTerm, repeats=True)


m_package.__init_metainfo__()
