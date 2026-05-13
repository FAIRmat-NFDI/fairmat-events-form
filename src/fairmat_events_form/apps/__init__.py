from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    Axis,
    Column,
    Dashboard,
    Layout,
    Menu,
    MenuItemTerms,
    SearchQuantities,
    WidgetHistogram,
    WidgetTerms,
)


class EventsAppEntryPoint(AppEntryPoint):
    pass


SCHEMA = 'fairmat_events_form.schema_packages.schema_package.ApplicantInformation'

# Indexed term path — same pattern as nomad-training-resources.
# Querying `fairmat_area_terms.value` lets a multi-area entry match when any
# of its values is selected (OR-match across areas).
Q_AREA = f'data.fairmat_area_terms.value#{SCHEMA}'
Q_ROLE = f'data.role_at_fairmat#{SCHEMA}'
Q_NAME = f'data.full_name#{SCHEMA}'

events_app_entry_point = EventsAppEntryPoint(
    name='Events Requests App',
    description='This app is to track the submitted\
          events requests by FAIRmat members',
    app=App(
        label='Events Requests',
        path='eventsapp',
        category='Use Cases',
        description='Track the events requests from FAIRmat members',
        search_quantities=SearchQuantities(
            include=[f'data.*#{SCHEMA}', f'metadata.*#{SCHEMA}']
        ),
        filters_locked={
            'entry_type': 'ApplicantInformation',
        },
        columns=[
            Column(
                quantity=Q_NAME,
                label='Name',
                selected=True,
            ),
            Column(
                quantity=Q_ROLE,
                label='Role',
                selected=True,
            ),
            Column(
                quantity=Q_AREA,
                label='Area',
                selected=True,
            ),
            Column(
                quantity=f'data.event_details.event_name#{SCHEMA}',
                label='Event name',
                selected=True,
            ),
            Column(quantity='entry_create_time', label='Creation Time', selected=True),
        ],
        menu=Menu(
            title='Terms Filters',
            items=[
                Menu(
                    title='Requestor Information',
                    items=[
                        MenuItemTerms(
                            quantity=Q_NAME,
                            title='Name',
                            show_input=True,
                        ),
                        MenuItemTerms(
                            quantity=Q_AREA,
                            title='FAIRmat Area',
                            show_input=False,
                        ),
                        MenuItemTerms(
                            quantity=Q_ROLE,
                            title='Role',
                            show_input=False,
                        ),
                    ],
                ),
                Menu(
                    title='Request Status',
                    items=[
                        MenuItemTerms(
                            quantity=f'data.status.status#{SCHEMA}',
                            title='Status',
                            show_input=False,
                        ),
                        MenuItemTerms(
                            quantity=f'data.status.reimbursement_source#{SCHEMA}',
                            title='Paid from',
                            show_input=False,
                        ),
                    ],
                ),
            ],
        ),
        dashboard=Dashboard(
            widgets=[
                WidgetTerms(
                    title='FAIRmat Area',
                    search_quantity=Q_AREA,
                    layout={
                        'md': Layout(w=6, h=4, x=0, y=0, minW=3, minH=3),
                        'lg': Layout(w=6, h=4, x=0, y=0, minW=3, minH=3),
                    },
                ),
                WidgetTerms(
                    title='Role',
                    search_quantity=Q_ROLE,
                    layout={
                        'md': Layout(w=6, h=4, x=6, y=0, minW=3, minH=3),
                        'lg': Layout(w=6, h=4, x=6, y=0, minW=3, minH=3),
                    },
                ),
                WidgetHistogram(
                    title='Event Expenses',
                    autorange=True,
                    nbins=30,
                    scale='linear',
                    x=Axis(
                        search_quantity=f'data.total_expenses#{SCHEMA}',
                        title='Total cost (€)',
                    ),
                    layout={'lg': Layout(minH=4, minW=6, h=4, w=6, y=4, x=0)},
                ),
                WidgetHistogram(
                    title='Submission date',
                    autorange=True,
                    nbins=30,
                    scale='linear',
                    x=Axis(
                        search_quantity=f'data.submission_date#{SCHEMA}', title='Date'
                    ),
                    layout={'lg': Layout(minH=4, minW=6, h=4, w=6, y=4, x=6)},
                ),
            ]
        ),
    ),
)
