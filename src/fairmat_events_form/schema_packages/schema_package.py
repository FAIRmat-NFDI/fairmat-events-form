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
        label='To be paid from'
        )

class EventExpenses(ArchiveSection):
    """
    A subsection for providing the expected costs associated with the event.
    """
    intro_expenses = Quantity(
        type=str,
        label='Select one category for expenses from the dropdown menu above.',
    )

    # def normalize(self, archive, logger):
    #     """
    #     Compute total expenses automatically during normalization.
    #     """
    #     travel = self.travel_expenses_amount or 0
    #     accom = self.accommodation_expenses_amount or 0
    #     other = self.other_expenses_amount or 0
    #     self.total_expenses = travel + accom + other

class TransportationExpenses(EventExpenses):
        travel_method = Quantity(
        type=MEnum(
            'Train',
            'Flight',
            'Car',
            'Taxi',
            'Public transport',
            'Other'
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
        label='Tranportation Method',
        description='Costs associated to traveling to the conference venue'
        )
    
        travel_cost = Quantity(
            type=float,
            a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
            label='Cost (Euro)',
            description='Costs associated to traveling to the event venue'
            )
        
        travel_justification = Quantity(
            type=str,
            a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
            label='Justification (mandatory for 1st class train travel, flights, taxis,\
                  or business-class tickets)',
            description='Costs associated to traveling to the event venue'
            )       
class AccommodationExpenses(EventExpenses):
        accomodation_duration = Quantity(
            type=int,
            a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
            label='Number of nights',
            description='Number of accommodation nights needed'
            )

        accommodation_cost = Quantity(
            type=float,
            a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
            label='Cost (Euro)',
            description='Costs associated to traveling to the event venue'
            )
        
        accommodation_justification = Quantity(
            type=str,
            a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
            label='Justification (mandatory when this cost is above €90/night)',
            description='Costs associated to traveling to the event venue'
            )
        
        cost_night = Quantity(
             type=float,
             label= 'Cost per night'
        )
        
        def normalize(self, archive, logger):
            """
            Compute accomodation cost per night.
            """
            night= self.accomodation_duration or 1
            total_cost = self.accommodation_cost or 0
            self.cost_night = total_cost / night
class ConferenceExpenses(EventExpenses):
        conference_cost = Quantity(
            type=float,
            a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
            label='Registration fees (Euro)',
            description='Costs associated to traveling to the event venue'
            )    
class OtherExpenses(EventExpenses):
        other_expenses_description = Quantity(
            type=str,
            a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
            label='Cost description',
            description='Other costs associated with the event'
            )
        other_cost = Quantity(
            type=float,
            a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
            label='Other costs (Euro)',
            description='Other costs associated with the event'
            )
        other_costs_justification = Quantity(
            type=str,
            a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
            label='Justification',
            description='Costs associated to traveling to the event venue'
            )
class EventInformation(ArchiveSection):
    """
    An Entry for requesting an approval to attend an external event.
    """

    event_name = Quantity(
        type=str,
        a_eln=ELNAnnotation(
            component=ELNComponentEnum.StringEditQuantity),
        description='The Name of the event'
        )
    
    event_website = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.URLEditQuantity),
        description='Event Website',
        label='Event website',
        default='https://'
        )

    event_organizer_or_host = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description='Name of the organizing entity or host',
        label='Organizer/Host'
    )

    location= Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description='Location where the event takes place',
        label='Event location',
        
        )
    
    event_start_date = Quantity(
        type=Datetime,
        a_eln=ELNAnnotation(component=ELNComponentEnum.DateEditQuantity)
        )
    
    event_end_date = Quantity(
        type=Datetime,
        a_eln=ELNAnnotation(component=ELNComponentEnum.DateEditQuantity)
        )

    attendance_method = Quantity(
        type=MEnum(
            'In-person',
            'Virtual',
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
        description='Applicant FAIRmat Area'
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
        description='Applicant FAIRmat Area'
    )
    title_of_contribution = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description='Applicant FAIRmat Area'
    )

class ApplicantInformation(Schema):
    """
    An Entry for requesting an approval to attend an external event.
    """

    m_def = Section(
        label='Event Participation Request',
        categories=[UseCaseElnCategory],
    )

    full_name = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description='Requestor full name',
        label='Full name (First, Last)'
        )
    
    email = Quantity(
        type=str,
        a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity),
        description='Applicant Email',
        label='Email'

        )
    
    submission_date = Quantity(
        type=Datetime,
        a_eln=dict(component='DateTimeEditQuantity'),
        description='Date of submission',
        label='Submission date'
        )
    role_at_fairmat = Quantity(
        type=MEnum(
            'Principal Investigator',
            'Coordinator',
            'Coworker',
            'Collaborator',
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
        description='Role in FAIRmat',
        label='Role in FAIRmat'
    )

    fairmat_area = Quantity(
        type=MEnum(
            'A: Synthesis',
            'B: Experiments',
            'C: Computations',
            'D: Infrastructure',
            'E: Usecases',
            'F: Outreach',
            'G: Adminstration',
        ),
        a_eln=ELNAnnotation(component=ELNComponentEnum.EnumEditQuantity),
        label='FAIRmat Area',
        description='Applicant FAIRmat Area'
    )

    summary = Quantity(
        type=str,
        label='Summary (Please don''t modify this field, it will \
            be automatically generated from your input)',
        a_eln=ELNAnnotation(component=ELNComponentEnum.RichTextEditQuantity),
        description='Auto-generated summary shown in overview',
    )

    total_expenses = Quantity(
         type=float,
         a_eln=ELNAnnotation(component=ELNComponentEnum.NumberEditQuantity),
         label='Total expenses'

    )


    def normalize(self, archive, logger):
        super().normalize(archive, logger)

        details = self.event_details if hasattr(self, 'event_details') else None
        expenses = self.expected_expenses if hasattr(self, 'expected_expenses') else []
        status = self.status if hasattr(self, 'status') else None
        parts = []
        total_cost = 0.0

        # --- Event details ---
        if details:
            if details.event_name:
                parts.append(f"<b>Event:</b> {details.event_name}")
            if details.event_start_date and details.event_end_date:
                parts.append(f"<b>Date:</b> {details.event_start_date.date()}\
                              – {details.event_end_date.date()}")
            elif details.event_start_date:
                parts.append(f"<b>Date:</b> {details.event_start_date.date()}")
            if details.location:
                parts.append(f"<b>Location:</b> {details.location}")
            if details.participation_type:
                parts.append(f"<b>Participation:</b> {details.participation_type}")

        # --- Expenses ---
        if expenses:
            parts.append("<b>Expected expenses</b>")
            for exp in expenses:

                expense_fields = [
                    ("travel_cost", "Travel cost", "travel_method"),
                    ("accommodation_cost", "Accommodation", None),
                    ("conference_cost", "Registration fees", None),
                    ("other_cost", "Other costs", "other_expenses_description"),
                ]

                for attr, field_label, note_attr in expense_fields:
                    if hasattr(exp, attr) and getattr(exp, attr):
                        value = getattr(exp, attr)
                        note = getattr(exp, note_attr) if note_attr and \
                            hasattr(exp, note_attr) and getattr(exp, note_attr) else ""
                        suffix = f" ({note})" if note else ""
                        parts.append(f"• {field_label}: €{value:.2f}{suffix}")
                        total_cost += value

        # --- Total and status ---
        if total_cost > 0:
            parts.append(f"<b>Total expenses:</b> €{total_cost:.2f}")
            self.total_expenses = total_cost

        if status and status.status:
            parts.append(f"<b>Status:</b> {status.status}")

        self.summary = "<br>".join(parts)




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


m_package.__init_metainfo__()
