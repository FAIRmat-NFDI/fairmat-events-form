from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class EventsSchemaPackageEntryPoint(SchemaPackageEntryPoint):
    parameter: int = Field(0, description='Custom configuration parameter')

    def load(self):
        from fairmat_events_form.schema_packages.schema_package import m_package

        return m_package


events_schema_package_entry_point = EventsSchemaPackageEntryPoint(
    name='fairmat_events_form',
    description='Events form entry point configuration.',
)
