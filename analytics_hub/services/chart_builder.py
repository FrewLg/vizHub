from django.db.models import Avg


FIELD_MAP = {
    "year": "year",
    "location": "location__name",
    "cause": "cause__name",
    "sex": "sex__name",
    "age_group": "age_group__name",
    "facility_category": "facility_category__name",
}


def build_chart_data(queryset, config):

    x_axis = FIELD_MAP.get(config.x_axis)

    if not x_axis:
        return {"labels": [], "datasets": []}

    if not config.series_dimension:

        data = (
            queryset
            .values(x_axis)
            .annotate(value=Avg("value"))
            .order_by(x_axis)
        )

        return {
            "labels": [row[x_axis] for row in data],
            "datasets": [
                {
                    "label": "Value",
                    "data": [
                        float(row["value"] or 0)
                        for row in data
                    ]
                }
            ]
        }

    series_field = FIELD_MAP.get(config.series_dimension)

    records = (
        queryset
        .values(x_axis, series_field)
        .annotate(value=Avg("value"))
    )

    labels = sorted({
        row[x_axis]
        for row in records
        if row[x_axis]
    })

    series_values = sorted({
        row[series_field]
        for row in records
        if row[series_field]
    })

    datasets = []

    for series in series_values:

        dataset = []

        for label in labels:

            matching = next(
                (
                    r for r in records
                    if r[x_axis] == label
                    and r[series_field] == series
                ),
                None
            )

            dataset.append(
                float(matching["value"])
                if matching else 0
            )

        datasets.append({
            "label": series,
            "data": dataset
        })

    return {
        "labels": labels,
        "datasets": datasets
    }