def content():
    TITLE_DICT = {"Introduction":[["Features", "/features"],
                                ["Upgrades", "/upgrades"],
                                ["Out of the Box", "/out-of-the-box"]]}
    DEST_DICT = {"Destinations":[["Delhi", "India"],
                                ["New York", "USA"],
                                ["California", "USA"],
                                ["Toronto", "Canada"],
                                ["Vancouver", "Canada"],
                                ["Brasilia", "Brazil"],
                                ["Pretpria", "South Africa"],
                                ["Abu Dhabi", "UAE"],
                                ["London", "UK"],
                                ["Paris", "France"],
                                ["Beijing", "China"],
                                ["Hong Kong", "China"],
                                ["Thailand", "Bangkok"],
                                ["Tokyo", "Japan"],
                                ["Kuala Lumpur", "Malasya"],
                                ["Canberra", "Australia"],
                                ["Moscow", "Russia"],
                                ["Seoul", "South Korea"]]}

    inr_rate = 15               # Rate / Km
    usd_rate = 0.25

    return DEST_DICT

content()
