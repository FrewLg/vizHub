"""
Management command: load_boundaries
====================================
Reads all four admin-level shapefiles and populates (or refreshes) the
LocationGeometry table by matching each shapefile feature to an existing
Location row.

Matching strategy (in order):
  1. By pcode   — Location.code  == adm{N}_pcode
  2. By name    — Location.name  == adm{N}_name  (case-insensitive)

Usage
-----
  python manage.py load_boundaries
  python manage.py load_boundaries --level region   # only one level
  python manage.py load_boundaries --dry-run        # preview without saving
"""

import json
import logging
from pathlib import Path

import geopandas as gpd
from shapely.geometry import mapping
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from analytics_hub.models import Location, LocationGeometry

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Level configuration
# ---------------------------------------------------------------------------
# Maps our CLI level name → (shapefile stem, Location.level value,
#                             pcode field, name field)
LEVEL_CONFIG = {
    "country": (
        "eth_admin0",
        "country",
        "adm0_pcode",
        "adm0_name",
    ),
    "region": (
        "eth_admin1",
        "region",
        "adm1_pcode",
        "adm1_name",
    ),
    "zone": (
        "eth_admin2",
        "zone",
        "adm2_pcode",
        "adm2_name",
    ),
    "woreda": (
        "eth_admin3",
        "woreda",
        "adm3_pcode",
        "adm3_name",
    ),
}


class Command(BaseCommand):
    help = "Load admin boundary geometries from shapefiles into LocationGeometry"

    def add_arguments(self, parser):
        parser.add_argument(
            "--level",
            choices=list(LEVEL_CONFIG.keys()),
            default=None,
            help="Only process one level (default: all four)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            default=False,
            help="Preview matches without writing to the database",
        )
        parser.add_argument(
            "--shp-dir",
            default=None,
            help=(
                "Path to the directory containing the shapefiles "
                "(default: <BASE_DIR>/eth_admin_boundaries.shp)"
            ),
        )

    # ------------------------------------------------------------------
    def handle(self, *args, **options):
        shp_dir = Path(
            options["shp_dir"] or
            Path(settings.BASE_DIR) / "eth_admin_boundaries.shp"
        )
        if not shp_dir.is_dir():
            raise CommandError(f"Shapefile directory not found: {shp_dir}")

        dry_run = options["dry_run"]
        levels = (
            [options["level"]] if options["level"]
            else list(LEVEL_CONFIG.keys())
        )

        total_created = total_updated = total_skipped = 0

        for level_key in levels:
            shp_stem, db_level, pcode_field, name_field = LEVEL_CONFIG[level_key]
            shp_path = shp_dir / f"{shp_stem}.shp"

            if not shp_path.exists():
                self.stderr.write(self.style.WARNING(
                    f"  [{level_key}] shapefile not found, skipping: {shp_path}"
                ))
                continue

            self.stdout.write(f"\n── {level_key.upper()} ({shp_path.name}) ──")
            created, updated, skipped = self._process_level(
                shp_path, db_level, pcode_field, name_field, dry_run
            )
            total_created += created
            total_updated += updated
            total_skipped += skipped

        tag = "[DRY RUN] " if dry_run else ""
        self.stdout.write(self.style.SUCCESS(
            f"\n{tag}Finished — "
            f"created: {total_created}  "
            f"updated: {total_updated}  "
            f"skipped (no match): {total_skipped}"
        ))

    # ------------------------------------------------------------------
    def _process_level(self, shp_path, db_level, pcode_field, name_field, dry_run):
        gdf = gpd.read_file(shp_path).to_crs(epsg=4326)

        created = updated = skipped = 0

        with transaction.atomic():
            for _, row in gdf.iterrows():
                pcode = row.get(pcode_field) or ""
                name  = row.get(name_field)  or ""
                geom_dict = mapping(row["geometry"])

                location = self._find_location(pcode, name, db_level)

                if location is None:
                    self.stdout.write(self.style.WARNING(
                        f"  NO MATCH  pcode={pcode!r}  name={name!r}"
                    ))
                    skipped += 1
                    continue

                if dry_run:
                    action = (
                        "UPDATE" if hasattr(location, "geometry") else "CREATE"
                    )
                    self.stdout.write(
                        f"  {action}  {location.name!r}  (pk={location.pk})"
                    )
                    continue

                obj, was_created = LocationGeometry.objects.update_or_create(
                    location=location,
                    defaults={"geojson": geom_dict},
                )
                if was_created:
                    created += 1
                    self.stdout.write(
                        f"  CREATED  {location.name!r}  (pk={location.pk})"
                    )
                else:
                    updated += 1
                    self.stdout.write(
                        f"  UPDATED  {location.name!r}  (pk={location.pk})"
                    )

            if dry_run:
                # Roll back so nothing is committed
                transaction.set_rollback(True)

        return created, updated, skipped

    # ------------------------------------------------------------------
    @staticmethod
    def _find_location(pcode: str, name: str, db_level: str):
        """
        Try to find a Location by pcode first, then by name.
        Handles the fact that the DB level values may differ slightly
        from the shapefile level key (e.g. 'Regional' vs 'region').
        """
        # Level aliases stored in the DB vary; search broadly then filter
        qs = Location.objects.filter(level__iexact=db_level)

        # 1. pcode match
        if pcode:
            loc = qs.filter(code__iexact=pcode).first()
            if loc:
                return loc

        # 2. exact name match (case-insensitive)
        if name:
            loc = qs.filter(name__iexact=name).first()
            if loc:
                return loc

        # 3. name match without level constraint (covers level naming mismatches)
        if name:
            loc = Location.objects.filter(name__iexact=name).first()
            if loc:
                return loc

        return None
