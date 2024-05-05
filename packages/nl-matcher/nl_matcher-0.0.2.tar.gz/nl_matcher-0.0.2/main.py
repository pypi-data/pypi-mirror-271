from location_matcher import LocationMatcher

location_matcher = LocationMatcher()

text = "Even na 22.00 uur kreeg de politie een melding vanuit de trein. Daarop werd Amersfoort Centraal ontruimd. Toen de man niet op het waarschuwingsschot reageerde, hebben agenten hem getaserd en gearresteerd."

locations = location_matcher(text)

for span in locations:
    print({
        "start_char": span.start_char,
        "end_char": span.end_char,
        "text": span.text,
    })
