from django.db import models


class CoordinateField(models.DecimalField):
    description = "Store coordinates of a location"

    def __init__(self, *args, **kwargs):
        kwargs["max_digits"] = 9
        kwargs["decimal_places"] = 6
        kwargs["null"] = True
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)
