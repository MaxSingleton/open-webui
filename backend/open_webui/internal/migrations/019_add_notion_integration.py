"""Peewee migrations -- 019_add_notion_integration.py.

This migration creates the notion_integration table to store per-project Notion database mappings.
"""

import peewee as pw
from peewee_migrate import Migrator

def migrate(migrator: Migrator, database: pw.Database, *, fake: bool = False):
    # Create table to store Notion integration mapping per project
    @migrator.create_model
    class NotionIntegration(pw.Model):
        project_id = pw.TextField(primary_key=True)
        database_id = pw.TextField(null=True)
        created_at = pw.DateTimeField(null=True)
        updated_at = pw.DateTimeField(null=True)

        class Meta:
            table_name = "notion_integration"

def rollback(migrator: Migrator, database: pw.Database, *, fake: bool = False):
    # Remove the notion_integration table
    migrator.remove_model("notion_integration")