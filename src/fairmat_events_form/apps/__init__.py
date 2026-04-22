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
)


class EventsAppEntryPoint(AppEntryPoint):
    pass


schema = 'fairmat_events_form.schema_packages.schema_package.ApplicantInformation'

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
            include=[f'data.*#{schema}', f'metadata.*#{schema}']
        ),
        filters_locked={
            'entry_type': 'ApplicantInformation',
        },
        columns=[
            Column(
                quantity=f'data.full_name#{schema}',
                label='Name',
                selected=True,
            ),
            Column(
                quantity=f'data.role_at_fairmat#{schema}',
                label='Role',
                selected=True,
            ),
            Column(
                quantity=f'data.fairmat_area#{schema}',
                label='Area',
                selected=True,
            ),
            Column(
                quantity=f'data.event_details.event_name#{schema}',
                label='Event name',
                selected=True,
            ),
            Column(quantity='entry_create_time', label='Creation Time', selected=True),
        ],
        menu=Menu(
            title='Terms Filters',
            items=[
                # filter by Area
                Menu(
                    title='Requestor Information',
                    items=[
                        MenuItemTerms(
                            quantity=f'data.full_name#{schema}',
                            title='Name',
                            show_input=False,
                        ),
                        MenuItemTerms(
                            quantity=f'data.fairmat_area#{schema}',
                            title='FAIRmat Area',
                            show_input=False,
                        ),
                        MenuItemTerms(
                            quantity=f'data.role_at_fairmat#{schema}',
                            title='role',
                            show_input=False,
                        ),
                    ],
                ),
                Menu(
                    title='Request Status',
                    items=[
                        MenuItemTerms(
                            quantity=f'data.status.status#{schema}',
                            title='Status',
                            show_input=False,
                        ),
                        MenuItemTerms(
                            quantity=f'data.status.reimbursement_source#{schema}',
                            title='Paid from',
                            show_input=False,
                        ),
                    ],
                ),
            ],
        ),
        dashboard=Dashboard(
            widgets=[
                WidgetHistogram(
                    title='Event Expenses',
                    autorange=True,
                    nbins=30,
                    scale='linear',
                    x=Axis(
                        search_quantity=f'data.total_expenses#{schema}',
                        title='Total cost (€)',
                    ),
                    layout={'lg': Layout(minH=4, minW=6, h=4, w=6, y=0, x=0)},
                ),
                WidgetHistogram(
                    title='Submission date',
                    autorange=True,
                    nbins=30,
                    scale='linear',
                    x=Axis(
                        search_quantity=f'data.submission_date#{schema}', title='Date'
                    ),
                    layout={'lg': Layout(minH=4, minW=6, h=4, w=6, y=0, x=6)},
                ),
            ]
        ),
    ),
)
